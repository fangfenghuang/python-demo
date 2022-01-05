# encoding: utf-8

import uuid
from gevent import pywsgi
from kubernetes import client, config
from kubernetes.leaderelection import leaderelection
from kubernetes.leaderelection.resourcelock.configmaplock import ConfigMapLock
from kubernetes.leaderelection import electionconfig
from conf import *
from app import app


config.load_kube_config(config_file=K8S_CONFIG)

candidate_id = uuid.uuid4()

lock_name = "python-demo"

lock_namespace = "default"


def on_start():
    print("I am leader now")
    server = pywsgi.WSGIServer(('0.0.0.0', SERVICE_PORT), app)
    server.serve_forever()


if __name__ == '__main__':
    config = electionconfig.Config(ConfigMapLock(lock_name, lock_namespace, candidate_id), lease_duration=17,
                               renew_deadline=15, retry_period=5, onstarted_leading=on_start,
                               onstopped_leading=None)

    leaderelection.LeaderElection(config).run()
    print("Exited leader election")
