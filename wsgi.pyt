from server import app 


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=7788,
            ssl_context=(
                "./static/server/server-cert.pem",
                "./static/server/server-key.pem",
            ))
