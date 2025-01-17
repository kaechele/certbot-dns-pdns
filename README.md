# Certbot DNS Authenticator for PowerDNS

PowerDNS DNS Authenticator plugin for [Certbot](https://certbot.eff.org). This
plugin uses the PowerDNS HTTP API to request modifications for the DNS-01
challenge.

A design goal of this plugin is to use the minimal amount of custom code to
achieve integration with PowerDNS.

As such it uses the existing Lexicon-based DNS framework in Certbot and may not
work for you if you are using intermediary tools, such as PowerDNS-Admin or a
restrictively configured reverse proxy, to implement access restrictions or
Role-based Access controls (RBAC).

## Installation

1. Install the plugin from PyPI

   ```shell
   pip install certbot-dns-pdns
   ```

   Alternatively you can also install both certbot and the plugin using `pipx`:

   ```shell
   pipx install certbot certbot-dns-pdns
   ```

2. Verify that the plugin is installed:

   ```shell
   $ certbot plugins

   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   * dns-pdns
   Description: Obtain certificates using a DNS TXT record (if you are using
   PowerDNS for DNS).
   Interfaces: Authenticator, Plugin
   Entry point: EntryPoint(name='dns-pdns',
   value='certbot_dns_pdns.dns_pdns:Authenticator', group='certbot.plugins')

   [...]
   ```

## Usage

Create a credentials file to use with this plugin:

`~/pdns-credentials.ini`

```ini
dns_pdns_endpoint = https://pdns-api.example.com
dns_pdns_api_key = <Your API Key>
dns_pdns_server_id = localhost # see https://doc.powerdns.com/authoritative/http-api/server.html
dns_pdns_disable_notify = false # Disable notification of secondaries after record changes
```

The available configuration options correspond to the
[DNS-Lexicon settings for the PowerDNS provider](https://dns-lexicon.readthedocs.io/en/latest/configuration_reference.html#powerdns).

Run Certbot using the plugin as the authenticator:

```shell
certbot certonly \
    --authenticator dns-pdns \
    --dns-pdns-credentials ~/pdns-credentials.ini \
    ...
```

> [!NOTE]
>
> Since this plugin communicates with PowerDNS via the HTTP API make sure that
> the `SOA-EDIT-API` setting for your zone is set to a value that results in an
> increase of the SOA serial (i.e. the setting exists in your domain metadata).
> Otherwise the changes made to the zone by this plugin will not propagate to
> any secondaries you may have configured, causing the certificate challenge to
> potentially fail.
>
> For more information see the
> [PowerDNS documentation](https://doc.powerdns.com/authoritative/domainmetadata.html#soa-edit-api)

## Contributing

Pull requests are welcome. GitHub automatically runs `pre-commit` on any pull
requests, so you may want to enable `pre-commit` on your end, so your PR doesn't
fail these checks.

This repository uses [Conventional Commits](https://www.conventionalcommits.org)
commit messages. Check the git log for examples on how to use them.

## License

Apache License 2.0

## Maintainer

- Felix Kaechele <felix@kaechele.ca>
