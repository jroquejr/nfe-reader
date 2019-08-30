NF_READER_ENDPOINT = "/"
HEALTH_CHECK_ENDPOINT = "/healthcheck"

FAKE_NFE_URL = "http://nfe.sefaz.ba.gov.br/servicos/nfce/qrcode.aspx?p=29190710230480000300650020046429391067584521|2|1|1|02DEF8AF9895079E1B6C439CD83A91A04E0F04E0"
FAKE_WRONG_NFE_URL = "http://nfe.sefaz.ba.gov.br/servicos/nfce/qrcode.aspx?p=23213123123|2|1|1|02DEF8AF9895079E1B6C439CD83A91A04E0F04E0"


def test_api_healthcheck(client):
    response = client.get(HEALTH_CHECK_ENDPOINT)
    response_json = response.get_json()
    assert response.status_code == 200
    assert "status" in response_json
    assert response_json.get("status") is True


def test_api_nfe_reader_with_no_url_code(client):
    response = client.post(NF_READER_ENDPOINT, json={})
    assert response.status_code == 400
    assert response.json.get("message") == "Missing URL QRCODE"


def test_api_nfe_reader_when_get_internal_error(client):
    response = client.post(NF_READER_ENDPOINT, json={"url_qrcode": FAKE_WRONG_NFE_URL})
    assert response.status_code == 500
    assert response.json.get("message") == "Couldnt read the URL"


def test_api_nfe_reader(client):
    response = client.post(NF_READER_ENDPOINT, json={"url_qrcode": FAKE_NFE_URL})
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json()
