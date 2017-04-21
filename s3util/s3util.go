package s3util

import(
  "time"
  "os"
  "context"
  "fmt"
  "bytes"
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
  svc *s3.S3
}


func NewBucket(credFile string, profile string, region string) *Bucket{
  creds := credentials.NewSharedCredentials(credFile, profile)
  sess := session.Must(session.NewSession(&aws.Config{
    Region: aws.String(region),
    Credentials: creds,
  }))
  svc := s3.New(sess)
  return &Bucket{svc}
}

func (buck *Bucket) Upload(data []byte, bucket string, dstPath string) {
  ctx := context.Background()
  var cancelFn func()
  timeout, err := time.ParseDuration(TIMEOUT)
  if err != nil {
    fmt.Println(err)
    os.Exit(1)
  }
  if timeout > 0 {
    ctx, cancelFn = context.WithTimeout(ctx, timeout)
  }
  defer cancelFn()

  resp, err := buck.svc.PutObjectWithContext(ctx, &s3.PutObjectInput{
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