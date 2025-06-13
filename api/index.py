from bookmyseat.wsgi import application  # Replace with your actual project name

def handler(request, context):
    return application(
        environ=request.environ,
        start_response=context.start_response
    )
