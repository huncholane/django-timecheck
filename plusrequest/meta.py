from typing import TypedDict


class DefaultMeta(TypedDict, total=False):
    """The default meta items in a django request."""

    CONTENT_LENGTH: str
    """The length of the request body (as a string)."""
    CONTENT_TYPE: str
    """The MIME type of the request body."""
    HTTP_ACCEPT: str
    """Acceptable content types for the response."""
    HTTP_ACCEPT_ENCODING: str
    """Acceptable encodings for the response."""
    HTTP_ACCEPT_LANGUAGE: str
    """Acceptable languages for the response."""
    HTTP_HOST: str
    """The HTTP Host header sent by the client."""
    HTTP_REFERER: str
    """The referring page, if any."""
    HTTP_USER_AGENT: str
    """The client’s user-agent string."""
    QUERY_STRING: str
    """The query string, as a single (unparsed) string."""
    REMOTE_ADDR: str
    """The IP address of the client."""
    REMOTE_HOST: str
    """The hostname of the client."""
    REMOTE_USER: str
    """The user authenticated by the web server, if any."""
    REQUEST_METHOD: str
    """A string such as "GET" or "POST"."""
    SERVER_NAME: str
    """The hostname of the server."""
    SERVER_PORT: str


class DefaultHeaders(TypedDict, total=False):
    """Headers from the default meta"""

    accept: str
    """Acceptable content types for the response."""
    accept_encoding: str
    """Acceptable encodings for the response."""
    HTTP_ACCEPT_LANGUAGE: str
    """Acceptable languages for the response."""
    HTTP_HOST: str
    """The HTTP Host header sent by the client."""
    HTTP_REFERER: str
    """The referring page, if any."""
    HTTP_USER_AGENT: str
    """The client’s user-agent string."""


class PlusMeta(TypedDict, total=False):
    """Optional headers commonly used in extended HTTP request metadata."""

    HTTP_AUTHORIZATION: str | None
    """Standard header for bearer tokens, API keys, basic auth, etc."""
    HTTP_X_API_KEY: str | None
    """Custom API key used instead of Authorization."""
    HTTP_API_KEY: str | None
    """Alternate spelling, seen in some legacy systems."""
    HTTP_X_SESSION_ID: str | None
    """Session identifier, often used in mobile apps or sticky auth."""
    HTTP_SESSION: str | None
    """Alternate field for session ID."""
    HTTP_X_CLIENT_ID: str | None
    """Identifies the application or user making the request."""
    HTTP_X_CLIENT_SECRET: str | None
    """Used in OAuth-style flows to authenticate the client."""
    HTTP_X_APP_TOKEN: str | None
    """App-level token separate from user access."""
    HTTP_X_REFRESH_TOKEN: str | None
    """Used for token refresh flows in OAuth 2.0 systems."""
    HTTP_X_TOKEN: str | None
    """A token for api request"""
    HTTP_TOKEN: str | None
    """A token for api request"""
    HTTP_LASTUPDATED: str | None
    """Custom header indicating the client's last update timestamp (e.g., ISO 8601)."""
    HTTP_IF_NONE_MATCH: str | None
    """ETag validator for conditional requests (used for caching)."""
    HTTP_IF_MODIFIED_SINCE: str | None
    """Timestamp used to check if the resource has changed since the client's last version."""
    HTTP_X_REQUEST_ID: str | None
    """Unique identifier for tracing requests across services or logs."""
    HTTP_X_REAL_IP: str | None
    """Actual client IP address, typically added by a reverse proxy."""
    HTTP_X_FORWARDED_FOR: str | None
    """Comma-separated list of IPs forwarded through proxies (first is original client)."""
    HTTP_X_DEVICE_ID: str | None
    """Custom header identifying the client's device (mobile or desktop apps)."""
    HTTP_X_PLATFORM: str | None
    """Platform identifier such as 'ios', 'android', 'web', etc."""
    HTTP_X_APP_VERSION: str | None
    """Version string of the client app, useful for feature gating or debugging."""
    HTTP_ORIGIN: str | None
    """Origin of the request, used in CORS validation."""
    HTTP_DNT: str | None
    """Do Not Track header, indicating user's tracking preference ('1' or '0')."""
    HTTP_SEC_CH_UA: str | None
    """User-Agent Client Hint header, sent by modern browsers like Chrome."""


class Meta(DefaultMeta, PlusMeta):
    """A typed dict for the default meta items in django as well as some other common header fields."""
