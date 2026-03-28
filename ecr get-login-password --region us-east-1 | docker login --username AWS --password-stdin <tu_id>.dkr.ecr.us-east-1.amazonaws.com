{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:047719650114:repository/procesar",
        "registryId": "047719650114",
        "repositoryName": "procesar",
        "repositoryUri": "047719650114.dkr.ecr.us-east-1.amazonaws.com/procesar",
        "createdAt": "2026-03-28T15:57:29.226000+00:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": false
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
