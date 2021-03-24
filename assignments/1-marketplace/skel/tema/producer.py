"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from .marketplace import Marketplace
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace : Marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, kwargs=kwargs)
        self.products = products
        self.marketplace = marketplace
        self.time = republish_wait_time

    def run(self):
        self.id = self.marketplace.register_producer()
        while True:
            if self.marketplace.finish.is_set():
                break

            for product in self.products:
                if not self.marketplace.publish(self.id, product[0]):
                    sleep(self.time)
                else:
                    sleep(product[2])
                    # print('{} produced {}'.format(self.id, product[0]))
