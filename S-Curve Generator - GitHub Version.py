import math
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def transform_to_s_curve(data, lowerBound, upperBound):
    cumulative_data = np.cumsum(data)  # Calculate cumulative sum of the original data

    # Normalize the cumulative data between 0 and 1
    normalized_data = (cumulative_data - cumulative_data.min()) / (cumulative_data.max() - cumulative_data.min())

    # Calculate the shifting factor for centering the peak
    shifting_factor = 0.5 - normalized_data.mean()

    # Avoid divide by zero error
    normalized_data[normalized_data == 0] = 1e-15
    normalized_data[normalized_data == 1] = 1 - 1e-15

    # Find the index where the highest value should occur (closer to the center)
    highest_value_index = len(data) // 3 + len(data) // 6

    # Apply modified S-curve transformation to normalized data with the shifting factor and modified power function
    transformed_data = (np.tanh((normalized_data - 0.5 + shifting_factor) * 3) + 1) / 2

    # Adjust the transformed data to achieve the S-shape with the highest value closer to the center
    highest_value = transformed_data[highest_value_index]
    transformed_data[highest_value_index:] *= highest_value / transformed_data[highest_value_index]

    # Adjust the tail of the S-shape to decrease more aggressively towards the end
    tail_length = len(data) - highest_value_index
    tail_values = np.linspace(1, 0, tail_length)
    transformed_data[highest_value_index:] *= tail_values

    # Scale and shift the transformed data to fit within the range of 6-20
    transformed_data = lowerBound + (transformed_data - np.min(transformed_data)) * (upperBound - lowerBound) / (np.max(transformed_data) - np.min(transformed_data))

    # Scale the transformed data to match the sum of the original data
    transformed_data *= np.sum(data) / np.sum(transformed_data)

    return transformed_data

def sendEmail(body):
    user = "" #Input senders email address, if static just use a constant
    receiver = "" #Input recievers email address, again if static use constant value
    passcode = "" #Passcode generated from the senders email address provider to allow the email to be sent

    userMessage = body.split()
    userMessage = userMessage[0]

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = receiver
    msg['Subject'] = userMessage + ' Data for Outputs'
    message = body
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login(user, passcode)

    success = mailserver.sendmail(user, receiver, msg.as_string())
    if(success == {}):
        print("Message Successfully Sent")

    mailserver.quit()


while(True):
    expectedAverage = float(input("Enter the expected working average output for the duration: "))
    expectedWorkingDays = int(input("Enter the expected amount of working days for the duration: "))

    originalList = [expectedAverage] * expectedWorkingDays

    print(originalList, '\n\n')
    print("Sum of original list: ", round(sum(originalList), 3))

    lowerBound = expectedAverage * 0.5 #50% of the expected average output to start
    upperBound = expectedAverage * 1.64 #64% increase on the expected average for the peak running of the install 

    newList = transform_to_s_curve(originalList, lowerBound, upperBound)
    transformedListString = ''

    '''for new in newList:
        print(round(new,3), end=' ')
    print('\n\n')'''

    for new in newList:
        transformedListString += (str(round(new, 3)) + ' ')

    messageToSend = input('What would you like to include within your email: ')
    messageToSend += transformedListString
    sendEmail(messageToSend)

    
    