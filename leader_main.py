# encoding: utf-8

# 参考：python\kubernetes\base\leaderelection\example.py
import sys
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


def on_started():
    print("I am leader now！！！！")
    # server = pywsgi.WSGIServer(('0.0.0.0', SERVICE_PORT), app)
    # server.serve_forever()

def on_stopped():
    print("stop leading now！！！")
    sys.exit(1)

if __name__ == '__main__':
    config = electionconfig.Config(ConfigMapLock(lock_name, lock_namespace, candidate_id), lease_duration=30,
                               renew_deadline=15, retry_period=5, onstarted_leading=on_started,
                               onstopped_leading=on_stopped, release_on_cancel=True)

    leaderelection.LeaderElection(config).run()
    print("Exited leader election")
