# DnScan

This repository contains small scripts created during penetration tests for various things, that may be useful to other people.

These scripts have generally been written quickly and are unlikely to have proper error handling, or to have been thoroughly tested.

Use at your own risk.

# Scripts

## [aspnet_identity_v2_to_john.py](aspnet_identity_v2_to_john.py)

Convert ASP.NET Identity v2 hashes into a format that can be cracked with John. Hashes can be extract with the following SQL query:

```sql
SELECT CONCAT(UserName, ':', PasswordHash) FROM AspNetUsers
```

## [extract_ldap_hashes.py](extract_ldap_hashes.py)

Takes the output from `dbscan` or `ldapsearch` and extracts usernames and password hashes into a format that can be used with John, to allow easy password auditing for 389-ds, FreeIPA and Red Hat Identity Manager (IdM). The [FreeIPA Password Auditing](https://www.codasecurity.co.uk/articles/freeipa-password-auditing/) article on the CODA website contains further details.

## [parse_pwdump_admins.py](parse_pwdump_admins.py)

Takes the output of [NtdsAudit](https://github.com/Dionach/NtdsAudit) and parses it into a CSV file that shows which *enabled* users belong to which privileged groups.

## [sourcescan.py](sourcescan.py)

A quick TCP port scanner that lets you specify a range of source ports to scan from.

Useful for identifying firewall rules that allow traffic from specific ports (such as 53 or 179).

The lists of source and target ports are defined inside the script in the `__main__` function.

