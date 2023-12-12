import httpx
import base64
import datetime


class AuthenticatedClient:
    """BeeYard client.

    This class can be initialized in multiple ways, depending on the login type the user wants to perform.

    Parameters
    ----------
    base_url : str
        The url to the Hive.
    username : str, optional
        Used if the grant_type is ``password``.
    password : str, optional
        Used if the grant_type is ``password``.
    grant_type : {'password', 'client_credentials'}
        Type of login to perform, by default "password".
    max_waiting_time_ms : int, optional
        Waiting time between subsequent calls, by default 0.
    client_id : str, optional
        Used if the grant_type is ``client_credentials``.
    client_secret : str, optional
        Used if the grant_type is ``client_credentials``.
    login_url : str, optional
        To be specified if login server is on different domain then Hive, by default None.
    use_token : bool, optional
        To be set True if a valid token is used instead of login, by default False., by default False.
    token : str or dict, optional
        Valid token, by default None.

    Attributes
    ----------
    token_headers : dict
        Is initialized by the constructor. It contains the valid token to be used to communicate with BeeYard.

    Examples
    --------
    >>> client = AuthenticatedClient("http://localhost:8018/hive/", "tester", "foobar")

    >>> # Using client credentials
    >>> client = AuthenticatedClient(
    >>>    "http://localhost:8018/hive/",
    >>>    grant_type="client_credentials",
    >>>    client_id="public.app",
    >>>    client_secret="barfoo",
    >>>    login_url="http://localhost:8018/id/",
    >>>)

    >>> #Using valid access token
    >>> client = AuthenticatedClient(
    >>>    "http://localhost:8018/hive/",
    >>>    use_token=True,
    >>>    token=valid_token,
    >>>)
    """

    def __init__(
        self,
        base_url,
        username="",
        password="",
        grant_type="password",
        max_waiting_time_ms=0,
        client_id="byard",
        client_secret="",
        login_url=None,
        use_token=False,
        token=None,
    ):
        """Initialize the client.

        Init method uses authenticate() method, or directly the token parameter if provided,
        to initialize the token_header attribute of the class.

        Parameters
        ----------
        base_url : str
        The url to the Hive.
        username : str, optional
            Used if the grant_type is ``password``.
        password : str, optional
            Used if the grant_type is ``password``.
        grant_type : {'password', 'client_credentials'}
            Type of login to perform, by default "password".
        max_waiting_time_ms : int, optional
            Waiting time between subsequent calls, by default 0.
        client_id : str, optional
            Used if the grant_type is ``client_credentials``.
        client_secret : str, optional
            Used if the grant_type is ``client_credentials``.
        login_url : str, optional
            To be specified if login server is on different domain then Hive, by default None.
        use_token : bool, optional
            To be set True if a valid token is used instead of login, by default False., by default False.
        token : str or dict, optional
            Valid token, by default None.
        """

        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.username = username
        self.password = password
        self.grant_type = grant_type
        self.delay = max_waiting_time_ms
        self.endpoint_auth: str = "/oauth/token/"
        self.client_id = client_id
        self.client_secret = client_secret
        self.login_url = login_url
        if use_token:
            if isinstance(token, dict):
                self.token_headers = token
            elif "Authorization" in token:
                self.token_headers = {"Authorization": f"Bearer {token.split(' ')[2]}"}
            else:
                self.token_headers = {"Authorization": f"Bearer {token}"}
        else:
            self.authenticate()

    def authenticate(self):
        """Authenticate the client.

        Returns
        -------
        bool
            Returns true if authentication is performed successfully.

        Raises
        ------
        Exception
            If grant_type is not recognized.
        Exception
            If authentication fails.
        """

        if self.grant_type == "password":
            data = {
                "grant_type": self.grant_type,
                "username": self.username,
                "password": self.password,
            }
            credentials = self.client_id + ":" + self.client_secret
            message_bytes = credentials.encode("ascii")
            base64_bytes = base64.b64encode(message_bytes)
            base64_credentials = base64_bytes.decode("ascii")
            header = {"Authorization": "Basic " + base64_credentials}
        elif self.grant_type == "client_credentials":
            data = {
                "grant_type": self.grant_type,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
            header = {}
        else:
            raise Exception(f"Grant type '{self.grant_type}' not recognized")
        if self.login_url is None:
            response = httpx.post(
                f"{self.base_url}{self.endpoint_auth}".replace("hive", "id"),
                data=data,
                headers=header,
            )
        else:
            response = httpx.post(
                f"{self.login_url}{self.endpoint_auth}",
                data=data,
                headers=header,
            )
        if response.status_code not in range(200, 300):
            raise Exception("Bad authenticate response")
        auth = "Bearer " + response.json()["access_token"]
        self.token_headers = {"Authorization": auth}
        return True

    def check_response(self, response):
        """Check status response from API.

        Parameters
        ----------
        response : Response
            Http response from API.

        Returns
        -------
        bool
            True if Response status is in range 200-300.

        Raises
        ------
        Exception
            Bad response if Response status is in range 400-500.
        Exception
            Bad response if Response status is in range 500-600.
        """
        if response.status_code in range(200, 300):
            return True
        if response.status_code in range(400, 500):
            raise Exception("Bad response: client exception -> %s" % response.text)
        if response.status_code in range(500, 600):
            raise Exception("Bad response: server exception -> %s" % response.text)

    def get(self, *args, **kwargs):
        """Performs HTTP GET request.

        Tries for ``delay`` seconds to reconnect in case of connection error.
        If response status is 401, it tries to re-authenticate the user.

        Returns
        -------
        Response
            Http response from API.
        """
        try:
            response = httpx.get(*args, **kwargs, timeout=None)
        except httpx.ConnectError:
            t1 = datetime.datetime.now()
            while ((datetime.datetime.now() - t1).total_seconds() * 1000) < self.delay:
                try:
                    httpx.get(*args, **kwargs, timeout=None)
                    break
                except httpx.ConnectError:
                    continue
            response = httpx.get(*args, **kwargs, timeout=None)
        if response.status_code == 401:
            self.authenticate()
            kwargs["headers"]["Authorization"] = self.token_headers["Authorization"]
            try:
                response = httpx.get(*args, **kwargs, timeout=None)
            except httpx.ConnectError:
                t1 = datetime.datetime.now()
                while (
                    (datetime.datetime.now() - t1).total_seconds() * 1000
                ) < self.delay:
                    try:
                        httpx.get(*args, **kwargs, timeout=None)
                        break
                    except httpx.ConnectError:
                        continue
                response = httpx.get(*args, **kwargs, timeout=None)
        self.check_response(response)
        return response

    def post(self, *args, **kwargs):
        """Performs HTTP POST request.

        Tries for ``delay`` seconds to reconnect in case of connection error.
        If response status is 401, it tries to re-authenticate the user.

        Returns
        -------
        Response
            Http response from API.
        """
        try:
            response = httpx.post(*args, **kwargs, timeout=None)
        except httpx.ConnectError:
            t1 = datetime.datetime.now()
            while ((datetime.datetime.now() - t1).total_seconds() * 1000) < self.delay:
                try:
                    httpx.post(*args, **kwargs, timeout=None)
                    break
                except httpx.ConnectError:
                    continue
            response = httpx.post(*args, **kwargs, timeout=None)
        if response.status_code == 401:
            self.authenticate()
            kwargs["headers"]["Authorization"] = self.token_headers["Authorization"]
            try:
                response = httpx.post(*args, **kwargs, timeout=None)
            except httpx.ConnectError:
                t1 = datetime.datetime.now()
                while (
                    (datetime.datetime.now() - t1).total_seconds() * 1000
                ) < self.delay:
                    try:
                        httpx.post(*args, **kwargs, timeout=None)
                        break
                    except httpx.ConnectError:
                        continue
                response = httpx.post(*args, **kwargs, timeout=None)
        self.check_response(response)
        return response

    def patch(self, *args, **kwargs):
        """Performs HTTP PATCH request.

        Tries for ``delay`` seconds to reconnect in case of connection error.
        If response status is 401, it tries to re-authenticate the user.

        Returns
        -------
        Response
            Http response from API.
        """
        try:
            response = httpx.patch(*args, **kwargs, timeout=None)
        except httpx.ConnectError:
            t1 = datetime.datetime.now()
            while ((datetime.datetime.now() - t1).total_seconds() * 1000) < self.delay:
                try:
                    httpx.patch(*args, **kwargs, timeout=None)
                    break
                except httpx.ConnectError:
                    continue
            response = httpx.patch(*args, **kwargs, timeout=None)
        if response.status_code == 401:
            self.authenticate()
            kwargs["headers"]["Authorization"] = self.token_headers["Authorization"]
            try:
                response = httpx.patch(*args, **kwargs, timeout=None)
            except httpx.ConnectError:
                t1 = datetime.datetime.now()
                while (
                    (datetime.datetime.now() - t1).total_seconds() * 1000
                ) < self.delay:
                    try:
                        httpx.patch(*args, **kwargs, timeout=None)
                        break
                    except httpx.ConnectError:
                        continue
                response = httpx.patch(*args, **kwargs, timeout=None)
        self.check_response(response)
        return response

    def delete(self, *args, **kwargs):
        """Performs HTTP DELETE request.

        Tries for ``delay`` seconds to reconnect in case of connection error.
        If response status is 401, it tries to re-authenticate the user.

        Returns
        -------
        Response
            Http response from API.
        """
        try:
            response = httpx.delete(*args, **kwargs, timeout=None)
        except httpx.ConnectError:
            t1 = datetime.datetime.now()
            while ((datetime.datetime.now() - t1).total_seconds() * 1000) < self.delay:
                try:
                    httpx.delete(*args, **kwargs, timeout=None)
                    break
                except httpx.ConnectError:
                    continue
            response = httpx.delete(*args, **kwargs, timeout=None)
        if response.status_code == 401:
            self.authenticate()
            kwargs["headers"]["Authorization"] = self.token_headers["Authorization"]
            try:
                response = httpx.delete(*args, **kwargs, timeout=None)
            except httpx.ConnectError:
                t1 = datetime.datetime.now()
                while (
                    (datetime.datetime.now() - t1).total_seconds() * 1000
                ) < self.delay:
                    try:
                        httpx.delete(*args, **kwargs, timeout=None)
                        break
                    except httpx.ConnectError:
                        continue
                response = httpx.delete(*args, **kwargs, timeout=None)
        self.check_response(response)
        return response

    def put(self, *args, **kwargs):
        """Performs HTTP PUT request.

        Tries for ``delay`` seconds to reconnect in case of connection error.
        If response status is 401, it tries to re-authenticate the user.

        Returns
        -------
        Response
            Http response from API.
        """
        try:
            response = httpx.put(*args, **kwargs, timeout=None)
        except httpx.ConnectError:
            t1 = datetime.datetime.now()
            while ((datetime.datetime.now() - t1).total_seconds() * 1000) < self.delay:
                try:
                    httpx.put(*args, **kwargs, timeout=None)
                    break
                except httpx.ConnectError:
                    continue
            response = httpx.put(*args, **kwargs, timeout=None)
        if response.status_code == 401:
            self.authenticate()
            kwargs["headers"]["Authorization"] = self.token_headers["Authorization"]
            try:
                response = httpx.put(*args, **kwargs, timeout=None)
            except httpx.ConnectError:
                t1 = datetime.datetime.now()
                while (
                    (datetime.datetime.now() - t1).total_seconds() * 1000
                ) < self.delay:
                    try:
                        httpx.put(*args, **kwargs, timeout=None)
                        break
                    except httpx.ConnectError:
                        continue
                response = httpx.put(*args, **kwargs, timeout=None)
        self.check_response(response)
        return response
