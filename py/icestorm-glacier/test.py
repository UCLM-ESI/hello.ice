#!/usr/bin/prego

from prego import Task, context

from _test import ComposeMixin, wait_until


class IceStormGlacier(ComposeMixin):
    def test_events_through_router(self):
        context.cwd = '$testdir'
        services = Task('services')
        services.command('docker compose up -d --build --remove-orphans', timeout=600)
        wait_until(services, 'docker compose logs subscriber | grep -q "waiting events"',
                   timeout=60)

        publisher = Task('publisher')
        publisher.command('make publish', timeout=120)
        wait_until(publisher,
                   'docker compose logs subscriber | grep -q "Event received: Hello World 9!"',
                   timeout=20)
