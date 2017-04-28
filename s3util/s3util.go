package s3util

import(
  "os"
  "bytes"
  "strings"
  "strconv"
  "log"
  "github.com/aws/aws-sdk-go/aws"
  "github.com/aws/aws-sdk-go/aws/awsutil"
  "github.com/aws/aws-sdk-go/aws/awserr"
  "github.com/aws/aws-sdk-go/aws/request"
  "github.com/aws/aws-sdk-go/service/s3"
  "github.com/aws/aws-sdk-go/aws/session"
  "github.com/aws/aws-sdk-go/aws/credentials"
)

const (
  TIMEOUT = "5s"
  LOG_FILE = "log"
)

type Bucket struct {
  Svc *s3.S3
  log *log.Logger
}

func NewBucket(credFile string, profile string, region string) *Bucket{
  creds := credentials.NewSharedCredentials(credFile, profile)
  sess := session.Must(session.NewSession(&aws.Config{
    Region: aws.String(region),
    Credentials: creds,
  }))
  svc := s3.New(sess)
  file, _ := os.OpenFile(LOG_FILE, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
  logger := log.New(file, "AWS LOG: ", log.Ldate|log.Ltime|log.Lshortfile)
  return &Bucket{
    Svc: svc,
    log: logger,
  }
}

func (buck *Bucket) Upload(data []byte, bucket string, dstPath string) {
  resp, err := buck.Svc.PutObject(&s3.PutObjectInput{
    Bucket: aws.String(bucket),
    Key:    aws.String(dstPath),
    Body:   bytes.NewReader(data),
    ContentLength: aws.Int64(int64(len(data))),
  })
  for err != nil {
    if aerr, ok := err.(awserr.Error); ok && aerr.Code() == request.CanceledErrorCode {
      buck.Log("Upload canceled due to timeout, %v\n", err)
    } else {
      buck.Log("Failed to upload object, %v\n", err)
    }
    buck.Log("Retrying uploading to AWS\n")
    resp, err = buck.Svc.PutObject(&s3.PutObjectInput{
      Bucket: aws.String(bucket),
      Key:    aws.String(dstPath),
      Body:   bytes.NewReader(data),
      ContentLength: aws.Int64(int64(len(data))),
    })
    buck.Log(resp.String())
  }

  buck.Log("Response %s", awsutil.StringValue(resp))
}

func (buck *Bucket) FindHighestMatrix(bucket string, prefix string) (string, int) {
  output, err := buck.Svc.ListObjects(&s3.ListObjectsInput{
    Bucket: &bucket,
    Prefix: &prefix,
  })
  for err != nil {
    buck.Log(err.Error())
    buck.Log("Retrying finding highest matrix from AWS\n")
    output, err = buck.Svc.ListObjects(&s3.ListObjectsInput{
      Bucket: &bucket,
      Prefix: &prefix,
    })
  }
  highest := 0
  var retkey, n string
  var nInt int
  for _, obj := range output.Contents {
    n = strings.Split(*(obj.Key), "/")[1]
    if n != "" {
      nInt, _ = strconv.Atoi(n)
    } else {
      nInt = 0
    }
    if nInt > highest {
      highest = nInt
      retkey = *(obj.Key)
    }
  }
  dataStruct, err := buck.Svc.GetObject(&s3.GetObjectInput{
    Bucket: &bucket,
    Key: &retkey,
  })
  for err != nil {
    buck.Log(err.Error())
    buck.Log("Retrying matrix retrieval from AWS\n")
    dataStruct, err = buck.Svc.GetObject(&s3.GetObjectInput{
      Bucket: &bucket,
      Key: &retkey,
    })
  }
  buf := new(bytes.Buffer)
  buf.ReadFrom(dataStruct.Body)
  matrix := buf.String()
  return matrix, highest
}

func (buck *Bucket) Log(message string, a ...interface{}) {
  buck.log.Printf(message, a...)
}