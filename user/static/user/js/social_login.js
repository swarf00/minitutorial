function buildQuery(params) {
    return Object.keys(params).map(function (key) {return key + '=' + encodeURIComponent(params[key])}).join('&')
}
function buildUrl(baseUrl, queries) {
    return baseUrl + '?' + buildQuery(queries)
}
function getQueryParameter(key) {
    queryParams = new URLSearchParams(location.search)
    return queryParams.get(key)
}

function naverLogin() {
    next = getQueryParameter('next')
    params = {
        response_type: 'code',
        client_id:'nfenn0pzKTlihOzu_h8S',
        redirect_uri: location.origin + '/user/login/social/naver/callback/' + (next ? '?next=' + next : ''),
        state: document.querySelector('[name=csrfmiddlewaretoken]').value
    }
    url = buildUrl('https://nid.naver.com/oauth2.0/authorize', params)
    location.replace(url)
}