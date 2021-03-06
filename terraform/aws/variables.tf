//-------------------------------------------------------------------
// Approzium settings
//-------------------------------------------------------------------

variable "download-url" {
    default = "https://github.com/cyralinc/approzium/releases/download/v0.2.0/linux_amd64.zip"
    description = "Download url for Approzium authenticator"
}

variable "extra-install" {
    default = ""
    description = "Extra commands to run in the install script"
}

variable "logs-file" {
    default = "/var/log/approzium.log"
    description = "Path to file where logs will be written"
}

//-------------------------------------------------------------------
// AWS settings
//-------------------------------------------------------------------

variable "ami" {
    default = "ami-7eb2a716"
    description = "AMI for Approzium instances"
}

variable "availability-zones" {
    default = "us-east-1a,us-east-1b"
    description = "Availability zones for launching the Approzium instances"
}

//-------------------------------------------------------------------
// Note: in production, we'd recommend an instance type that does not
//       use CPU credits, like an m4.large.
//-------------------------------------------------------------------
variable "instance_type" {
    default = "t2.micro"
    description = "Instance type for Approzium instances"
}

variable "instance_name" {
    default = "Approzium"
    description = "Instance name for Approzium"
}

//-------------------------------------------------------------------
// An example key name would be "ellen" as it appears in AWS, not "ellen.pem".
//-------------------------------------------------------------------
variable "key-name" {
    description = "SSH key name for Approzium instances"
}

//-------------------------------------------------------------------
// Example: "192.168. 100.0/24"
//-------------------------------------------------------------------
variable "cidr-block" {
    description = "The CIDR block that should be allowed to ingress into Approzium instances."
}
