from unittest.mock import MagicMock

class ProductsApiMock:

    def __init__(self):
        self.mock_v2_create_product = MagicMock()
        self.mock_v2_delete_product = MagicMock()
        self.mock_v2_get_product = MagicMock()
        self.mock_v2_list_products = MagicMock()
        self.mock_v2_replace_product = MagicMock()

    def v2_create_product(self, *args, **kwargs):
        """
        This method mocks the original api ProductsApi.v2_create_product with MagicMock.
        """
        return self.mock_v2_create_product(self, *args, **kwargs)

    def v2_delete_product(self, *args, **kwargs):
        """
        This method mocks the original api ProductsApi.v2_delete_product with MagicMock.
        """
        return self.mock_v2_delete_product(self, *args, **kwargs)

    def v2_get_product(self, *args, **kwargs):
        """
        This method mocks the original api ProductsApi.v2_get_product with MagicMock.
        """
        return self.mock_v2_get_product(self, *args, **kwargs)

    def v2_list_products(self, *args, **kwargs):
        """
        This method mocks the original api ProductsApi.v2_list_products with MagicMock.
        """
        return self.mock_v2_list_products(self, *args, **kwargs)

    def v2_replace_product(self, *args, **kwargs):
        """
        This method mocks the original api ProductsApi.v2_replace_product with MagicMock.
        """
        return self.mock_v2_replace_product(self, *args, **kwargs)

