# Query URL
QUEUE_URL="http://localhost:4566/000000000000/login-queue"

# CSV file to store the results
CSV_FILE="user_logins.csv"
echo "user_id,device_type,ip,device_id,locale,app_version" >> "$CSV_FILE"

# Receive and process messages from the queue
while true; do
  # Receive messages from the queue
  RESPONSE=$(awslocal sqs receive-message --queue-url "$QUEUE_URL")

  # Check if there are no more messages
  if [[ $(jq -r '.Messages[0].ReceiptHandle' <<< "$RESPONSE") == "" ]]; then
    break
  fi

  # Process each message
  MESSAGES=$(jq -c '.Messages[]' <<< "$RESPONSE")
  while IFS= read -r MESSAGE; do
    # Process the message as per your application logic
    BODY=$(jq -r '.Body' <<< "$MESSAGE")
    RES=$(echo "$BODY" | jq -r '"\(.user_id),\(.device_type),\(.ip),\(.device_id),\(.locale),\(.app_version)"')
    echo "Received message: $RES"

    # Append the message to the JSON file
    echo "$RES" >> "$CSV_FILE"

    # Delete the message from the queue
    RECEIPT_HANDLE=$(jq -r '.ReceiptHandle' <<< "$MESSAGE")
    awslocal sqs delete-message --queue-url "$QUEUE_URL" --receipt-handle "$RECEIPT_HANDLE"
  done <<< "$MESSAGES"
done