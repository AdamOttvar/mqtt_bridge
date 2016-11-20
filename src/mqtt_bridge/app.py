# -*- coding: utf-8 -*-
from __future__ import absolute_import

import inject
import paho.mqtt.client as mqtt
import rospy

from .util import lookup_object


def create_config(mqtt_client):
    def config(binder):
        binder.bind(mqtt.Client, mqtt_client)
    return config


def mqtt_bridge_node():
    # init node
    rospy.init_node('mqtt_bridge_node')

    # load parameters
    params = rospy.get_param("~", {})
    mqtt_params = params.pop("mqtt", {})
    conn_params = mqtt_params.pop("connection")

    # create mqtt client
    mqtt_client_factory_name = rospy.get_param(
        "~mqtt_client_factory", ".mqtt_client:default_mqtt_client_factory")
    mqtt_client_factory = lookup_object(mqtt_client_factory_name)
    mqtt_client = mqtt_client_factory(mqtt_params)

    # dependency injection
    config = create_config(mqtt_client)
    inject.configure(config)

    # configure and start MQTT Client
    mqtt_client.on_connect = _on_connect
    mqtt_client.on_disconnect = _on_disconnect
    mqtt_client.connect(**conn_params)
    mqtt_client.loop_start()

    # register shutdown callback and spin
    rospy.on_shutdown(mqtt_client.disconnect)
    rospy.on_shutdown(mqtt_client.loop_stop)
    rospy.spin()


def _on_connect(client, userdata, flags, response_code):
    rospy.loginfo('MQTT connected')


def _on_disconnect(client, userdata, response_code):
    rospy.loginfo('MQTT disconnected')


__all__ = ['mqtt_bridge_node']