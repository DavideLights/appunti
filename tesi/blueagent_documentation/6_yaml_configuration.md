# IaC Specification: Challenge Configuration & Data Models

## 1. Pydantic v2 Data Models

BlueAgent validates all challenge declarations and verification payloads using Pydantic v2:

```python
from typing import List, Dict, Optional, Literal, Any
from pydantic import BaseModel, Field

class CommandSpec(BaseModel):
    """Specification of an individual verification or readiness command."""
    target: Literal["container", "verifier"] = "container"
    container_name: Optional[str] = None       # Required if target == 'container'
    cmd: List[str]
    env: Dict[str, str] = Field(default_factory=dict)
    timeout: int = Field(15, ge=1, le=300)

class ContainerSpec(BaseModel):
    """Specification of an application system container."""
    name: str
    image: str
    ip_suffix: int = Field(..., ge=2, le=254)  # .1 = Gateway, .255 = Broadcast
    limits_cpu: str = "1"
    limits_memory: str = "256MB"

class VerifierSpec(BaseModel):
    """Optional ephemeral test runner container for black-box network checks."""
    image: str = "curlimages/curl:latest"
    ip_suffix: int = 250
    limits_cpu: str = "1"
    limits_memory: str = "256MB"

class ChallengeConfig(BaseModel):
    """Full configuration for challenge deployment and verification."""
    challenge_id: str
    team_k: int = Field(..., ge=0, le=254)
    verify_internet_access: bool = False
    verifier: Optional[VerifierSpec] = None    # None = in-container checks only
    containers: List[ContainerSpec]
    readiness_commands: List[CommandSpec] = Field(default_factory=list)
    verify_commands: List[CommandSpec]

class VerifyResultResp(BaseModel):
    """API response returned upon verification completion."""
    success: bool                              # True if test execution pipeline completed
    passed: bool                               # True if all verification checks succeeded
    message: str
    details: Optional[Dict[str, Any]] = None

class TeamCreateReq(BaseModel):
    """Payload to register a new team and allocate network namespaces."""
    team_k: int = Field(..., ge=0, le=254)
    name: str = Field(..., min_length=1, max_length=128)
    ctfd_team_id: Optional[int] = Field(default=None, ge=0)

class TeamMemberCreateReq(BaseModel):
    """Payload to generate a WireGuard configuration for an individual team member."""
    name: str = Field(..., min_length=1, max_length=128)
    ctfd_user_id: Optional[int] = Field(default=None, ge=0)
    ctfd_team_id: Optional[int] = Field(default=None, ge=0)
    team_name: Optional[str] = None
    public_key: Optional[str] = None

class TeamMemberWG(BaseModel):
    """Persisted WireGuard client configuration record for a team member."""
    member_id: str
    team_id: int
    team_k: int
    name: str
    client_ip: str
    public_key: str
    ctfd_user_id: Optional[int] = None
    private_key: Optional[str] = None
    preshared_key: Optional[str] = None
    config_path: Optional[str] = None
    config_text: Optional[str] = None
    created_at: datetime

class PeerStats(BaseModel):
    """WireGuard peer status and bandwidth telemetry for a team member."""
    member_id: str
    ctfd_user_id: Optional[int] = None
    name: str
    client_ip: str
    public_key: str
    endpoint: Optional[str] = None
    allowed_ips: str
    latest_handshake: int = 0
    transfer_rx: int = 0
    transfer_tx: int = 0
    persistent_keepalive: str = "off"
    online: bool = False
```

---

## 2. Declarative Challenge Descriptor (`challenge.yaml`)

```yaml
challenge_id: "patch-web-sqli"
title: "SQL Injection and Web Server Patch Management"
description: "SQLi mitigation challenge on Nginx + Python Flask + MySQL stack"
verify_internet_access: false   # Enable/disable NAT uplink inside ephemeral OVN sandbox

# Optional: Ephemeral test runner container for black-box network checks
verifier:
  image: "python:3.12-slim"
  ip_suffix: 250
  limits_cpu: "1"
  limits_memory: "256MB"

containers:
  - name: "database"
    image: "debian-12-mysql-master"
    ip_suffix: 3                # Maps to 10.k.1.3 (gateway 10.k.1.1)
    limits_cpu: "1"
    limits_memory: "512MB"

  - name: "server"
    image: "ubuntu-2204-flask-master"
    ip_suffix: 2                # Maps to 10.k.1.2
    limits_cpu: "1"
    limits_memory: "256MB"

readiness_commands:             # Health checks executed at initial deploy before marking ready
  - target: "container"
    container_name: "database"
    cmd: ["mysqladmin", "ping", "-h", "127.0.0.1"]
    timeout: 15
  - target: "container"
    container_name: "server"
    cmd: ["curl", "-s", "http://127.0.0.1:8080/health"]
    timeout: 10

verify_commands:                # Executed inside ephemeral OVN sandbox
  # 1. In-Container integrity check
  - target: "container"
    container_name: "server"
    cmd: ["systemctl", "is-active", "--quiet", "flask-app"]
    timeout: 5

  # 2. Black-box network exploit check from verifier runner
  - target: "verifier"
    cmd: ["python3", "/opt/checker/test_exploit_sqli.py", "--target", "10.k.1.2"]
    env:
      FLAG_KEY: "test_flag_secret"
    timeout: 15
```
