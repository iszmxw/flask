from flask import Flask
from flask import request
import collection
import json

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    page = request.args.get("page")
    if page is None:
        return {"code": 500, "msg": "请传递 page 页数"}
    else:
        page = "1"
    ok = collection.Start(page)
    if ok:
        return {"code": 200, "msg": "ok", "data": json.loads(ok)}
    else:
        return {"code": 500, "msg": "redis缓存失败"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
