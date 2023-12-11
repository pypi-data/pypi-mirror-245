# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-jsonschema unit tests for Pyramid JSON API."""

import base64
from datetime import date
from unittest import skip
from urllib.parse import urljoin

import jsonschema
from mock import patch

from pyramid.config import Configurator

from cubicweb import Binary, ValidationError
from cubicweb.devtools import BASE_URL
from cubicweb_web.devtools.testlib import PyramidWebCWTC, PyramidWebTestApp
from cubicweb_jsonschema import VIEW_ROLE
from cubicweb_jsonschema.entities.ijsonschema import (
    jsonschema_adapter,
)


class TestAppNoCSRF(PyramidWebTestApp):
    """Overloads TestApp to avoid csrf verification
    not implemented in FranceArchives so far.
    """

    def post(
        self,
        route,
        params=None,
        do_not_grab_the_crsf_token=True,
        do_not_inject_origin=True,
        **kwargs,
    ):
        return super(TestAppNoCSRF, self).post(
            route, params, do_not_grab_the_crsf_token, do_not_inject_origin, **kwargs
        )

    def post_json(
        self,
        route,
        params=None,
        do_not_grab_the_crsf_token=True,
        do_not_inject_origin=True,
        **kwargs,
    ):
        return super(TestAppNoCSRF, self).post_json(
            route, params, do_not_grab_the_crsf_token, do_not_inject_origin, **kwargs
        )

    def put_json(
        self,
        route,
        params=None,
        do_not_grab_the_crsf_token=True,
        do_not_inject_origin=True,
        **kwargs,
    ):
        return super(TestAppNoCSRF, self).put_json(
            route, params, do_not_grab_the_crsf_token, do_not_inject_origin, **kwargs
        )

    def delete(
        self,
        route,
        params="",
        do_not_grab_the_crsf_token=True,
        do_not_inject_origin=True,
        **kwargs,
    ):
        return super().delete(
            route, params, do_not_grab_the_crsf_token, do_not_inject_origin, **kwargs
        )


class BaseTC(PyramidWebCWTC):
    settings = {
        "cubicweb.bwcompat": False,
        "pyramid.debug_notfound": True,
        "cubicweb.auth.authtkt.session.secret": "x",
        "cubicweb.auth.authtkt.persistent.secret": "x",
        "cubicweb.session.secret": "x",
        "cubicweb.pyramid.enable_csrf": "no",
        "cubicweb.includes": [
            "cubicweb.pyramid.auth",
            "cubicweb.pyramid.session",
        ],
    }

    def includeme(self, config):
        config.include("cubicweb_jsonschema.api")

    def setUp(self):
        super(BaseTC, self).setUp()
        pyramid_config = Configurator(settings=self.settings)

        pyramid_config.registry["cubicweb.repository"] = self.repo
        pyramid_config.include("cubicweb.pyramid")
        pyramid_config.set_default_csrf_options(require_csrf=False)

        self.includeme(pyramid_config)
        self.pyr_registry = pyramid_config.registry
        self.webapp = TestAppNoCSRF(
            pyramid_config.make_wsgi_app(),
            extra_environ={"wsgi.url_scheme": "https"},
            admin_login=self.admlogin,
            admin_password=self.admpassword,
        )


class EntitiesTC(BaseTC):
    @skip("todo")
    def test_post_json_file_upload(self):
        data = {
            "login": "bob",
            "upassword": "bob",
            "picture": [
                {
                    "data": "data:text/xml;name=test;base64,{}".format(
                        base64.b64encode("hello")
                    ),
                }
            ],
        }
        self.webapp.login()
        resp = self.webapp.post_json(
            "/cwuser/", data, status=201, headers={"Accept": "application/json"}
        )
        with self.admin_access.cnx() as cnx:
            entity = cnx.find("CWUser", login="bob").one()
            self.assertTrue(entity.picture)
            photo = entity.picture[0]
            self.assertEqual(photo.read(), "hello")
        self.assertEqual(resp.location, "https://localhost:80/CWUser/%d" % entity.eid)

    @skip("todo")
    def test_post_json_file_upload_badrequest(self):
        self.webapp.login()
        for rtype, value in [
            ("unknown", [{"data": "who cares?"}]),
            ("picture", [{"data": "badprefix:blah blah"}]),
            ("picture", {"data": "not in a list"}),
        ]:
            data = {rtype: value}
            with self.subTest(**data):
                data["login"] = "bob"
                data["upassword"] = "bob"
                # Rely on "status=400" for test assertion.
                self.webapp.post_json(
                    "/CWUser/", data, status=400, headers={"Accept": "application/json"}
                )

    def test_get_related(self):
        with self.admin_access.cnx() as cnx:
            book = cnx.create_entity("Book", title="title")
            author = cnx.create_entity("Author", name="bob", reverse_author=book)
            jschema = (
                self.vreg["adapters"]
                .select(
                    "IJSONSchema", cnx, entity=author, rtype="author", role="object"
                )
                .view_schema()
            )
            cnx.commit()
        url = "/book/%s/author" % book.eid
        res = self.webapp.get(url, headers={"accept": "application/json"})
        related = res.json
        expected = [
            {
                "type": "author",
                "id": str(author.eid),
                "title": "bob",
            }
        ]
        with self.admin_access.cnx() as cnx:
            collection_mapper = cnx.vreg["mappers"].select(
                "jsonschema.collection", cnx, etype="Author"
            )
            jschema = collection_mapper.jsl_field(VIEW_ROLE).get_schema()
        jsonschema.validate(related, jschema)
        self.assertEqual(related, expected)

    def test_post_related_bad_identifier(self):
        with self.admin_access.cnx() as cnx:
            book = cnx.create_entity("Book", title="title")
            cnx.commit()
        self.webapp.login()
        url = "/book/%s/author" % book.eid
        res = self.webapp.post_json(
            url, ["a"], status=400, headers={"accept": "application/json"}
        )
        self.assertIn("invalid target identifier(s)", res.json["message"])

    @skip("todo in 1.8.1")
    def test_post_related_bad_role(self):
        with self.admin_access.cnx() as cnx:
            author = cnx.create_entity("Author", name="bob")
            cnx.commit()
        self.webapp.login()
        url = "/author/%s/author" % author.eid
        res = self.webapp.post_json(
            url, [], status=404, headers={"accept": "application/json"}
        )
        self.assertIn(
            "relation author-subject not found on Author", res.json["message"]
        )

    def test_post_related_entity_notfound(self):
        self.webapp.login()
        url = "/book/999/author"
        self.webapp.post_json(
            url, [], status=404, headers={"accept": "application/json"}
        )

    def test_post_related_bad_target(self):
        with self.admin_access.cnx() as cnx:
            book = cnx.create_entity("Book", title="title")
            cnx.commit()
            cwuser_eid = cnx.find("CWUser", login="admin")[0][0]
        self.webapp.login()
        url = "/book/%s/author" % book.eid
        self.webapp.post_json(
            url, [str(cwuser_eid)], status=400, headers={"accept": "application/json"}
        )

    def test_put_with_incomplete_data(self):
        """A PUT request *replaces* entity attributes, so if fields are
        missing from JSON request body, respective attributes are reset.
        """
        with self.admin_access.cnx() as cnx:
            entity = cnx.create_entity(
                "Photo", data=Binary(b"plop"), flash=True, exposure_time=1.23
            )
            cnx.create_entity(
                "Thumbnail", data=Binary(b"plip"), reverse_thumbnail=entity
            )
            cnx.commit()
        self.webapp.login()
        url = "/photo/{}/".format(entity.eid)
        self.webapp.put_json(
            url,
            {"data": "plip", "media_type": "jpeg"},
            headers={"Accept": "application/json"},
        )
        with self.admin_access.cnx() as cnx:
            entity = cnx.entity_from_eid(entity.eid)
            self.assertEqual(entity.data.getvalue(), b"plip")
            self.assertEqual(entity.media_type, "jpeg")
            # 'thumbnail' absent from request body, we should get ().
            self.assertEqual(entity.thumbnail, ())
            self.assertFalse(cnx.find("Thumbnail"))
            # 'flash' has a default value, we should get this back.
            self.assertEqual(entity.flash, False)
            # 'exposure_time' absent from request body, we should get None.
            self.assertIsNone(entity.exposure_time)

    def test_get_related_sort(self):
        """Sort by modification_date ascending and descending"""
        with self.admin_access.cnx() as cnx:
            author = cnx.create_entity("Author", name="bob")
            book1 = cnx.create_entity(
                "Book",
                title="1",
                publication_date=date(1976, 3, 1),
                author=author,
            )
            book2 = cnx.create_entity(
                "Book",
                title="1",
                publication_date=date(1977, 3, 1),
                author=author,
            )
            cnx.commit()

        ascending = [book1.title, book2.title]
        descending = ascending[::-1]
        for sort, expected in [
            ("publication_date", ascending),
            ("-publication_date", descending),
        ]:
            with self.subTest(sort=sort):
                url = "/author/%s/publications?sort=%s" % (author.eid, sort)
                res = self.webapp.get(url, headers={"accept": "application/json"})
                entities = res.json
                self.assertEqual(len(entities), 2)
                ids = [d["title"] for d in entities]
                self.assertEqual(ids, expected)

    def test_add_related(self):
        """POST on /<etype>/<eid>/relationships/<rtype> with primary entity as
        subject of <rtype>.
        """
        with self.admin_access.repo_cnx() as cnx:
            book = cnx.create_entity("Book", title="tmp")
            cnx.commit()
        url = urljoin(BASE_URL, f"/book/{book.eid}/relationships/author")
        data = {
            "name": "bob",
        }
        self.webapp.login()
        res = self.webapp.post_json(
            url, data, status=201, headers={"accept": "application/json"}
        )
        entity = res.json
        with self.admin_access.cnx() as cnx:
            author_eid = cnx.find("Author").one().eid
            jschema = jsonschema_adapter(cnx, etype="Author").view_schema()
        self.assertEqual(res.location, urljoin(BASE_URL, f"/Author/{author_eid}"))
        jsonschema.validate(entity, jschema)
        self.assertEqual(entity["name"], "bob")
        with self.admin_access.cnx() as cnx:
            rset = cnx.execute(
                'Any A WHERE B author A, B eid %(b)s, A name "bob"', {"b": book.eid}
            )
        self.assertTrue(rset)

    @skip("todo in 1.8.1")
    def test_add_related_object(self):
        """POST on /<etype>/<eid>/relationships/<rtype> with primary entity as
        object of <rtype>.
        """
        with self.admin_access.repo_cnx() as cnx:
            author = cnx.create_entity("Author", name="bob")
            cnx.commit()
        url = urljoin(BASE_URL, f"/author/%s/relationships/{author.eid}")
        data = {
            "title": "introducing cubicweb-jsonschema",
        }
        self.webapp.login()
        res = self.webapp.post_json(
            url, data, status=201, headers={"accept": "application/json"}
        )
        entity = res.json
        return
        with self.admin_access.cnx() as cnx:
            book_eid = cnx.find("Book").one().eid
            jschema = jsonschema_adapter(cnx, etype="Book").view_schema()
        self.assertEqual(res.location, urljoin(BASE_URL, f"/Book/{book_eid}"))
        jsonschema.validate(entity, jschema)
        self.assertEqual(entity["title"], "introducing cubicweb-jsonschema")
        with self.admin_access.cnx() as cnx:
            rset = cnx.execute(
                "Any X WHERE X author A, A eid %(a)s,"
                ' X title "introducing cubicweb-jsonschema"',
                {"a": author.eid},
            )
        self.assertTrue(rset)

    def test_validationerror_additionalproperties(self):
        data = {
            "name": "bob",
            "born": "1986",
        }
        self.webapp.login()
        res = self.webapp.post_json(
            "/author/", data, status=400, headers={"Accept": "application/json"}
        )
        errors = res.json_body["errors"]
        # See https://github.com/Julian/jsonschema/issues/243
        hint = "'born' was unexpected"
        expected = [
            {
                "status": 422,
                "details": ("Additional properties are not allowed " "(%s)" % hint),
            }
        ]
        self.assertCountEqual(errors, expected)

    def test_validationerror_nosource(self):
        """Test validation_failed view with no specific source entry."""
        data = {
            "login": "bob",
            "upassword": "pass",
        }
        with patch(
            "cubicweb.req.RequestSessionBase.create_entity",
            side_effect=ValidationError(None, {None: "unmapped"}),
        ):
            self.webapp.login()
            res = self.webapp.post_json(
                "/cwuser/", data, status=400, headers={"Accept": "application/json"}
            )
            error = res.json_body["errors"][0]
            self.assertEqual(error["status"], 422)
            self.assertIn(
                "at least one relation in_group is ""required on CWUser", error["details"]
            )
            self.assertEqual(error["source"], {"pointer": "in_group"})


if __name__ == "__main__":
    import unittest

    unittest.main()
