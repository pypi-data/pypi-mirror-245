class MissingTenantUrlProviderError(Exception):
    """Error when a base URL is expected but unspecified."""

    pass


class MissingAppConfigTypeError(Exception):
    """Error when app config is expected but unspecified."""

    pass


class MalformedAppWebhookError(Exception):
    """Error when a webhook cannot be read by an app."""

    pass
