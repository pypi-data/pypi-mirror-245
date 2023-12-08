# -*- coding: utf-8 -*-
from test_base_package.utils.logger import logger

from requests import Session, Response


class HttpClient:

    def __init__(self):
        self.session = Session()

    def api_request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                    timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None,
                    json=None) -> Response:
        """
        :param method: 方法用于新的:class: ' Request '对象
        :param url: 新的:class: ' Request '对象的URL
        :param params
        :param data
        :param headers
        :param cookies
        :param files
        :param auth
        :param timeout
        :param allow_redirects
        :param proxies
        :param hooks
        :param stream
        :param verify
        :param cert
        :param json
        :return:
        """
        try:
            resp = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                cookies=cookies,
                files=files,
                auth=auth,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
                json=json)
            return resp
        except Exception as e:
            logger.error(e)
            # 请求异常测试错误

    def close(self) -> None:
        self.session.close()


http_client = HttpClient()
