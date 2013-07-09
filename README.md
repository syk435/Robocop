Robocop: Automatic Detection, Alert, and Response System using a Raspberry Pi and a Sony PS3 Webcam
 
 *beta proof-of-concept test: detect if UPS box is deposited at door, if so then text the user 
  image and link to livestream, and play thank you audio for mailman

1. Webcam detects for motion. Once motion is detected, code uses algorithm to look for extremely specific shade of
   brown that matches UPS box

2. If both requirements are met, then code sends link of livestream and an image via text to user

3. Audio clip plays "Thank you" to Mailman to signify the other party knows it was deliverd

4. Thus user has satisfaction of knowing package was delivered as well as proof (in case of dispute) and can check live
   feed to make sure package doesn't get damaged/stolen
