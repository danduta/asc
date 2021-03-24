"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from queue import Empty, Full, Queue
from threading import Condition, Event, Lock
from .product import Product


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.max_size = queue_size_per_producer
        self.producers = {}
        self.consumers = {}
        self.products = {}
        self.producers_lock = Lock()
        self.products_lock = Lock()
        self.finish = Event()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.producers_lock:
            id = len(self.producers)
            self.producers[id] = Queue(self.max_size)
        
        return id

    def publish(self, producer_id, product: Product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        with self.products_lock:
            if product not in self.products:
                # print('Adding {} to queue.'.format(product))
                self.products[product] = Queue(999)

        try:
            self.products[product].put(product)
            self.producers[producer_id].put(product, block=False)
            # print('PRODUCE', product, ':', self.products[product].qsize())
            # print(product, ':', self.producers[producer_id].qsize(), '.....', self.products[product].qsize())
        except Full:
            # print('FULL')
            return False

        return True


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.products_lock:
            id = 'cons' + str(len(self.consumers) + 1)
            self.consumers[id] = []
        
        return id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.products_lock:
            if product not in self.products:
                # print('Adding {} to queue.'.format(product))
                self.products[product] = Queue(999)

        try:
            self.products[product].get(block=False)
            # print('ADD', product, ':', self.products[product].qsize())
            with self.products_lock:
                self.consumers[cart_id].append(product)
        except Empty:
            # print('Not enough of {}'.format(product))
            return False

        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # print('{} trying to remove {}.'.format(cart_id, product))
        with self.products_lock:
            if product not in self.consumers[cart_id]:
                return
            self.consumers[cart_id].remove(product)
            # print(cart_id, self.consumers[cart_id])

        try:
            self.products[product].put(product, block=False)
        except Full:
            # print('FULL REMOVE')
            return

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        with self.products_lock:
            order = self.consumers[cart_id].copy()
            self.consumers[cart_id].clear()

        return order

    def mark_finish(self, cart_id):

        with self.products_lock:
            del self.consumers[cart_id]
            if len(self.consumers) == 0:
                self.finish.set()
