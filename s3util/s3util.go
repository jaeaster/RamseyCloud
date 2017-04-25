package s3util

import(
  "time"
  "os"
  "fmt"
  "bytes"
  "strings"
  "strconv"
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
)

type Bucket struct {
  Svc *s3.S3
}

func NewBucket(credFile string, profile string, region string) *Bucket{
  creds := credentials.NewSharedCredentials(credFile, profile)
  sess := session.Must(session.NewSession(&aws.Config{
    Region: aws.String(region),
    Credentials: creds,
  }))
  Svc := s3.New(sess)
  return &Bucket{Svc}
}

func (buck *Bucket) Upload(data []byte, bucket string, dstPath string) {
  resp, err := buck.Svc.PutObjectWithContext(ctx, &s3.PutObjectInput{
    Bucket: aws.String(bucket),
    Key:    aws.String(dstPath),
    Body:   bytes.NewReader(data),
    ContentLength: aws.Int64(int64(len(data))),
  })
  if err != nil {
    if aerr, ok := err.(awserr.Error); ok && aerr.Code() == request.CanceledErrorCode {
      fmt.Fprintf(os.Stderr, "Upload canceled due to timeout, %v\n", err)
    } else {
      fmt.Fprintf(os.Stderr, "Failed to upload object, %v\n", err)
    }
    os.Exit(1)
  }
  fmt.Printf("Response %s", awsutil.StringValue(resp))
}

func (buck *Bucket) FindHighestMatrix(bucket string, prefix string) (string, int) {
  output, err := buck.Svc.ListObjects(&s3.ListObjectsInput{
    Bucket: &bucket,
    Prefix: &prefix,
  })
  checkError(err)
  highest := 0
  var retkey, n string
  var nInt int
  for _, obj := range output.Contents {
    n = strings.Split(*(obj.Key), "/")[1]
    if n != "" {
      nInt, err = strconv.Atoi(n)
      checkError(err)
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
  checkError(err)
  buf := new(bytes.Buffer)
  buf.ReadFrom(dataStruct.Body)
  matrix := buf.String()
  return matrix, highest
}

func checkError(err error) {
  if err != nil {
    fmt.Fprintf(os.Stderr, "Fatal Error: %s", err.Error())
    os.Exit(1)
  }
}