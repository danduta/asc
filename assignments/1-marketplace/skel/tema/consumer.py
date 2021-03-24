"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from .marketplace import Marketplace
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace : Marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, kwargs=kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.time = retry_wait_time

    def run(self):
        self.id = self.marketplace.new_cart()
        for cart in self.carts:
            for operation in cart:
                # print(self.id, operation)
                if operation['type'] == 'add':
                    for _ in range(operation['quantity']):
                        while not self.marketplace.add_to_cart(self.id, operation['product']):
                            sleep(self.time)
                elif operation['type'] == 'remove':
                    for _ in range(operation['quantity']):
                        self.marketplace.remove_from_cart(self.id, operation['product'])
                        sleep(self.time)

            order = self.marketplace.place_order(self.id)
            for item in order:
                print('{} bought {}'.format(self.id, item))

        self.marketplace.mark_finish(self.id)

