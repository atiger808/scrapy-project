import requests
from getheaders import getheaders

login_url = 'https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0'
headers = getheaders()
data = {
    'loginId':'594542251@qq.com',
    'password2':'wsb..058491',
    'ua': '124#jyTy4JnsxG0xA57fDcJ6Q2FzyW4pSZERFGw1bbuGFGDxWqAdkfhPfWYn/yDHxt4wMVOb1brXNR3bB0Td8ERdFqB1aS7SXY91qoRKa00/+YAaeT2pdqOwQzozqqhGzarSFw6ygyfUnCmiEhtyxTgWTpgYWelP3hioxgiEXJ7Na5x80L5UtPRh4DChMO6j9z7KCpU9y69mBldJejJNS9gSu5p9drCaN6cn9DSR588iYEXOGPg3QRs/F0wSvCrwN67eqEn6+etd5OjDb8ZqnxeF6hj3MxMMY5xBDO1f1H+TtRu3nWWfg0BdIoYLOWPr9622M/GkUFGXub8kON0zURWus0gh8BoHM7naF1DSopRfAPfFjlGNw+Zwb4L8Pb7U5efL16NrQfs9lVGMFkTPrI9kzPwjVs3s9Oy6tCFJlWOllay+98vy55aJCbUIYV4UM/YYWzPKN5VmYEK4Ie3Uze40rQNhlkqBlNTz8e8/5xJNcKqyh1zb0jIBly0z6R9La+Sh56JxTdPOywK7RF+kxgprX3ikYIByAaevA1uPe+jVwzR7rZ2ZlMNn6KvBIZYLlm9/HpEtjpzCgTSd7ZWZlULJ4W4D7C9plmI4mfWZIqbug5Sd1Z2ZlMXng7OBInYXbw/2m4+ZI8LLgTSo1n2elUX2g7vtIZ/plw/IU3c1IMY+g/Md1ZIefIlZ+hPteC/LMrYem4+erJD9XgdFv/gLxMcYuukN+yTISA3E71iHT4onBP+nfEjJtpRTAuIxM49boh17y4k0nRiegNi5KCfyNoA0UL3hzO5SSTOBmxuB7QrrY8ofF/8nO5j7jKuqmPfreObFRr+ajIF40ZO/WXcC0oxQKs4c5Ybqc0JGCjJIw5lA52vNatO6u8goO10qngkav90kDb/Oe2cfDmqLIMFHGqnpBw0tshK0iDWOZuLwLDfIkjm8PXq4B9j3mWCXCjspHRHaV9Um1Wcy69nWYuWR6gNlKPW6AWlsoC70/2nDi0fbGd43LInhabexiT/eI7KCYufTT9uN/NltozvlPcPL/G7hgXhihfGrzliO6Z1HVA9fd1sOmM3WBtB4mfQ344GWb8WtDjpbXtk4i/patPNLzSM/vpcFBWy6xL08Sf20p0ylVF1LorZkhv5RlcuUiMw2VC7YP1vmkxyWrQ7IbLBkjyd5QJH1mhqa3+E63ON6I+7Jbl5AuErxIg9RkEPyzx4xUz+0DZtdNUSwrAsO5p13b7s2SUGPiQyWXGjreengnkuBKihUPm3amfIbdiRrc9TqjU6uU2C3aOcVv30uG7k9iCCP4mIIn6AqEIyIJ60JJEuCO/DDiphNGlhtq5mmMaZBjTeEAcEN2oOFt1oDKTXG//Nv4mjGH7H35gIK2+qyLpwdPy0Uml/ULROlgMARdQmxrdGq4iDj93a+w54CXESPQPebe6Wl+sSb4nxgH4ssLDFaKgosvg0jFvj07eR4K4AXE5vVpxWya5b4c0UQykZYg24mevxNzNlf0PC8LL7KsD2L0o4iXGRNPOBtT7ncAh5p1848pWYrarN/oes57Bp4A7zGPatFfYsrcMNgOpX/8RwxnPGHg337RKFj3xrcyiNXccvWyxR/9jhG3orJIiR9rdUIc+kFO4ViY/CQk2novoIjXzwjBvn2kXs3bz9GsnVNeZ5ZmVJ7albx4xeZp3Z8njzh3dtOWLW7fIs7wvh93PUZamVJL70jIKHIbBDpo04yE8wS9yBh5rRGE/9n5We2Czx05/NQ8X3Htu7/WFGPK+Mo3hgjQysDpPx=',
    '_csrf_token': 'EuM4URLxD427jKvL3Ny0GD',
    'umidToken': '1e1e2e0390ddab5ae130a72b6f0001110d1e058b',
    'hsiz': '1d76eb12cf3c804c8eeffdfb2acdf702'
}
res = requests.post(login_url, data=data)
print(res.text)