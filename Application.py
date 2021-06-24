Model trained sucessefully
Step 3 - Run Our Facial Recognition
cap.release()
sender_email = "sender's email"
receiver_email = "reciever email"
​
def send_email():
    subject = "Security Alet!! Theft Detected..."
    body = """Hey,
    We found this person in front of your laptop.
    We informed you about this in case of security issues.
    The photo is attached below, recognize him."""
    password = getpass(prompt="Type your password and press enter:")
​
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # message["Bcc"] = receiver_email  # Recommended for mass emails
​
    # Add body to email
    message.attach(MIMEText(body))
   # filename = "document.pdf"  # In same directory as script
​
    
    # Open PDF file in binary mode
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(open("detected.jpg", "rb").read())
​
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
​
    # Add header as key/value pair to attachment part
    part.add_header(
    "Content-Disposition",
    f"attachment; filename= detected.jpg",)
​
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
​
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            return 0
    except SMTPException as error:
        print ("Error!! Something went wrong")
            
def whatsapp():
    t = datetime.datetime.now()
    try:
        pywhatkit.sendwhatmsg('Whatapp active number with country code', 'This message has been sent as we have found the users face in front of our camera. Check your email for the picture of the user', t.hour, t.minute+1)
        return("Sent")
    except:
        print("An Unexpected Error Occured!!!")
## Using Facial Recognition..For Sending Mail!!     
face_classifier = cv2.CascadeClassifier('haar.xml')
​
def ec2():
    ec2 = boto3.resource('ec2')
​
​
    instances = ec2.create_instances(
         ImageId='ami-0ab4d1e9cf9a1215a',
         MinCount=1,
         MaxCount=1,
         InstanceType='t2.micro',
         KeyName='taskkey',
         SubnetId='subnet-01170c3e0709db1c9'
         
     )
    ec2_launch=instances[0].id
    ebs = ec2.create_volume(AvailabilityZone='us-east-1b', Size=5, VolumeType='gp2')
    vol_id= ebs.id
    time.sleep(30)
    
    volume = ec2.Volume(vol_id)
    ebs_attach = volume.attach_to_instance(
        Device='/dev/sdh',
        InstanceId= ec2_launch,
        VolumeId=vol_id
    )
​
​
def face_detector(img, size=0.5):
    # Convert image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return img, []
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi
​
# Open Webcam
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    image, face = face_detector(frame)
    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        results = task6_model.predict(face)
        if results[1] < 500:
            confidence = int( 100 * (1 - (results[1])/400) )
            display_string = str(confidence) + '% Confident it is User'
        cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2)      
        if confidence >=85:
            f=0
            if cv2.imwrite("detected.jpg",image):
                print("One Face Successfuly detected")
                print("try sending the Image via Mail...")
                send=send_email()
                if send == 0:
                    print("Email Send Succesfully\t\t",end=" ")
                    f=1
                else:
                    print("Something went wrong while sending you a Email...!!")
            break
        
        else:
            print("Come infront of the camera.....")
            #cv2.putText(image, "I dont know, who r u", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            #cv2.imshow('Face Recognition', image )
            
    except:
        print("No face found..Try again later")
        #cv2.putText(image, "No Face Found", (220, 120) , cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        #cv2.putText(image, "looking for face", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        #cv2.imshow('Face Recognition', image )
        pass
        
    if cv2.waitKey(100) == 13: #13 is the Enter Key
        break
        
cap.release()
cv2.destroyAllWindows()
if f==1:
    send_whatsapp=whatsapp()
    if send_whatsapp=='Sent':
        print('successfully executed')
    else:
        print('some thing went wrong')
    ec2()
    print('please check your aws console')
    
