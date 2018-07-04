from app import create_app
if __name__=='__main__':
    # app=create_app('testing')
    app=create_app('development')
    app.run(port=6007 ,debug=True)