# -*- mode:python; coding:utf-8; tab-width:4 -*-

from unittest import TestCase
import Ice
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
import Services

from hamcrest import assert_that, is_
from doublex import Stub
from server import ContainerI


class ContainerServantTests(TestCase):
    def setUp(self):
        self.sut = ContainerI()
        self.stub = Stub(Ice.Object)

    def test_link(self):
        self.sut.link("foo", self.stub)

        assert_that(self.sut.list(),
                    is_({"foo": self.stub}))

    def test_unlink(self):
        self.sut.link("foo", self.stub)

        self.sut.unlink("foo")

        assert_that(self.sut.list(), is_({}))

    def test_no_such_key(self):
        try:
            self.sut.unlink("foo")
            self.fail()
        except Services.NoSuchKey:
            pass

    def test_already_exists(self):
        self.sut.link("foo", self.stub)

        try:
            self.sut.link("foo", self.stub)
            self.fail()
        except Services.AlreadyExists:
            pass
