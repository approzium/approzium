package credmgrs

import (
	"encoding/json"
	"fmt"

	vault "github.com/hashicorp/vault/api"
)

// In Vault, a mount path is the path where a secrets engine has been
// mounted. This code supports mounts that have been added the following way:
// "$ vault secrets enable -path=approzium -version=1 kv"
// Someday we may wish to make this path configurable.
const mountPath = "approzium"

func newHashiCorpVaultCreds() (CredentialManager, error) {
	// This uses a default configuration for Vault. This includes reading
	// Vault's environment variables and setting them as a configuration.
	client, err := vault.NewClient(nil)
	if err != nil {
		return nil, err
	}

	// Check that we're able to communicate with Vault by doing a test read.
	if _, err := client.Logical().Read(mountPath); err != nil {
		return nil, err
	}
	return &hcVaultCredMgr{
		vaultClient: client,
	}, nil
}

type hcVaultCredMgr struct {
	vaultClient *vault.Client
}

func (h *hcVaultCredMgr) Password(identity DBKey) (string, error) {
	path := mountPath + "/" + identity.DBHost + ":" + identity.DBPort
	secret, err := h.vaultClient.Logical().Read(path)
	if err != nil {
		return "", err
	}

	// Please see tests for examples of the kind of secret data we'd expect
	// here.
	userData := secret.Data[identity.DBUser]
	userDataJSON, ok := userData.(string)
	if !ok {
		return "", fmt.Errorf("couldn't convert %s to a string, type is %T", userData, userData)
	}
	userDataMap := make(map[string]interface{})
	if err := json.Unmarshal([]byte(userDataJSON), &userDataMap); err != nil {
		return "", err
	}

	// Verify that the inbound IAM role is one of the IAM roles listed as appropriate.
	iamRolesRaw, ok := userDataMap["iam_roles"]
	if !ok {
		return "", fmt.Errorf("iam_roles not found in %s", userDataMap)
	}
	iamRoles, ok := iamRolesRaw.([]interface{})
	if !ok {
		return "", fmt.Errorf("could not convert %s to array, type is %T", iamRolesRaw, iamRolesRaw)
	}
	authorized := false
	for _, iamRoleRaw := range iamRoles {
		iamRole, ok := iamRoleRaw.(string)
		if !ok {
			return "", fmt.Errorf("couldn't convert %s to a string, type is %T", iamRoleRaw, iamRoleRaw)
		}
		if iamRole == identity.IAMArn {
			authorized = true
			break
		}
	}
	if !authorized {
		return "", ErrNotAuthorized
	}

	// Verification passed. OK to return the password.
	passwordRaw, ok := userDataMap["password"]
	if !ok {
		return "", fmt.Errorf("password not found in %s", userDataMap)
	}
	password, ok := passwordRaw.(string)
	if !ok {
		return "", fmt.Errorf("could not convert %s to string, type is %T", passwordRaw, passwordRaw)
	}
	return password, nil
}