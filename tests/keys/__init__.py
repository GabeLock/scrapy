from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives.hashes import SHA256
    from cryptography.hazmat.primitives.serialization import (
        Encoding,
        NoEncryption,
        PrivateFormat,
    )
    from cryptography.x509 import (
        CertificateBuilder,
        DNSName,
        Name,
        NameAttribute,
        SubjectAlternativeName,
        random_serial_number,
    )
    from cryptography.x509.oid import NameOID
except ImportError:  # pragma: no cover - cryptography missing in CI image
    def generate_keys() -> None:
        """cryptography is unavailable; TLS tests will be skipped."""

        return None

    default_backend = rsa = SHA256 = Encoding = NoEncryption = PrivateFormat = None
    CertificateBuilder = (
        DNSName
    ) = Name = NameAttribute = SubjectAlternativeName = random_serial_number = NameOID = None
else:

    # https://cryptography.io/en/latest/x509/tutorial/#creating-a-self-signed-certificate
    def generate_keys():
        folder = Path(__file__).parent

        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        (folder / "localhost.key").write_bytes(
            key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=NoEncryption(),
            ),
        )

        subject = issuer = Name(
            [
                NameAttribute(NameOID.COUNTRY_NAME, "IE"),
                NameAttribute(NameOID.ORGANIZATION_NAME, "Scrapy"),
                NameAttribute(NameOID.COMMON_NAME, "localhost"),
            ]
        )
        cert = (
            CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(random_serial_number())
            .not_valid_before(datetime.now(tz=timezone.utc))
            .not_valid_after(datetime.now(tz=timezone.utc) + timedelta(days=10))
            .add_extension(
                SubjectAlternativeName([DNSName("localhost")]),
                critical=False,
            )
            .sign(key, SHA256(), default_backend())
        )
        (folder / "localhost.crt").write_bytes(cert.public_bytes(Encoding.PEM))
