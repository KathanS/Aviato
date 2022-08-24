import logging
import razorpay
import json

import azure.functions as func

razorpay_client = razorpay.Client(auth=("<APP_ID>", "<APP_SECRET>"))

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    amount = 5100
    payment_id = request.form['razorpay_payment_id']
    razorpay_client.payment.capture(payment_id, amount)
    return json.dumps(razorpay_client.payment.fetch(payment_id))
