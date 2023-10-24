# Group Policy Preferences Passwords

Group Policy Preferences Passwords are a feature in Windows that allow administrators to configure and manage passwords for various resources, such as user accounts, local administrator accounts, and network shares. These passwords are stored in Group Policy Objects (GPOs) and can be deployed to multiple computers or users within a domain.

However, Group Policy Preferences Passwords pose a significant security risk. By default, these passwords are stored in an easily reversible format within the GPOs. This means that any user with access to the GPOs can potentially extract and decrypt the passwords, leading to unauthorized access to sensitive resources.

Attackers can exploit this security vulnerability by gaining access to the GPOs or by intercepting the communication between the domain controller and the client computers. Once they have the encrypted passwords, they can use various techniques to decrypt them, such as using publicly available tools or performing offline attacks.

To mitigate the security risk associated with Group Policy Preferences Passwords, it is recommended to use alternative methods for managing passwords, such as using Group Managed Service Accounts (gMSAs) or implementing strong password policies. Additionally, regularly reviewing and updating GPOs to remove any stored passwords can help minimize the exposure of sensitive credentials.

---

## Step by Step computation

### 1. Compute the NT hash of the password



## Example

```

```

## References
 - https://podalirius.net/en/articles/exploiting-windows-group-policy-preferences/
