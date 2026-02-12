# Quick Start Guide - Kosymbiosis CI/CD

This guide provides quick instructions for using the autonomous CI/CD system.

## Prerequisites

- GitHub account with access to this repository
- GitHub CLI (`gh`) installed (optional, for command-line access)

## Overview

The CI/CD system automatically:
- ✅ Validates NSR compliance on every commit
- ✅ Checks Lex Amoris principles
- ✅ Monitors resonance values
- ✅ Deploys to IPFS on merge to main
- ✅ Synchronizes Klimabaum anchor nodes
- ✅ Self-heals on deployment failures
- ✅ Updates documentation automatically

## Workflow Triggers

### Automatic Triggers

1. **On Push** (any branch)
   - Runs CI validation
   - Checks NSR threshold
   - Validates documentation
   
2. **On Pull Request** (to main/develop)
   - Full CI validation
   - Dependency security review
   - Code security scanning
   
3. **On Merge to Main**
   - CI validation
   - IPFS deployment
   - Klimabaum synchronization
   - Documentation update
   
4. **Daily** (00:00 UTC)
   - Security vulnerability scan

### Manual Triggers

#### Using GitHub UI

1. Go to **Actions** tab
2. Select workflow (e.g., "Kosymbiosis CD - Deployment & Self-Healing")
3. Click **Run workflow**
4. Select branch and options
5. Click **Run workflow** button

#### Using GitHub CLI

```bash
# Trigger deployment
gh workflow run kosymbiosis-cd.yml

# Trigger with specific type
gh workflow run kosymbiosis-cd.yml -f deployment_type=emergency

# Trigger security scan
gh workflow run kosymbiosis-security.yml

# Trigger documentation update
gh workflow run kosymbiosis-docs.yml
```

## Viewing Results

### GitHub UI

1. Go to **Actions** tab
2. Click on workflow run
3. Review job results
4. Download artifacts (reports, metrics, logs)

### GitHub CLI

```bash
# List recent runs
gh run list

# View specific workflow runs
gh run list --workflow=kosymbiosis-ci.yml

# View run details
gh run view <run-id>

# Download artifacts
gh run download <run-id>
```

## Understanding Results

### CI Validation ✅

**Workflow**: `kosymbiosis-ci.yml`

**Success Indicators**:
- ✅ NSR score >= 0.80
- ✅ Lex Amoris references found
- ✅ Resonance values configured
- ✅ Documentation present

**Failure Indicators**:
- ❌ NSR score < 0.80 (triggers RED_CODE VETO)
- ⚠️ Missing Lex Amoris documentation
- ⚠️ Resonance misconfiguration

### Deployment Status ✅

**Workflow**: `kosymbiosis-cd.yml`

**Success Indicators**:
- ✅ IPFS hash generated
- ✅ Content pinned
- ✅ Klimabaum nodes synced
- ✅ Gateway URL available

**Self-Healing Activated**:
- 🔧 Fallback to previous IPFS hash
- 🔧 Alternative node paths established
- ℹ️ Check self-healing log for details

## Artifacts

### Available Artifacts

All workflow runs produce artifacts:

1. **NSR Validation Report** (90 days)
   - NSR score details
   - Threshold comparison
   - Validation timestamp
   
2. **Resonance Metrics** (90 days)
   - Frequency measurements
   - H-Factor values
   - Configuration status
   
3. **IPFS Deployment Report** (365 days)
   - IPFS hash (CID)
   - Gateway URL
   - Deployment metadata
   
4. **Self-Healing Log** (365 days)
   - Recovery actions
   - Vakuum-Brücke status
   - Error details (if any)
   
5. **Deployment Metrics** (365 days)
   - Complete deployment summary
   - Job status
   - NSR and resonance values
   
6. **Security Report** (90 days)
   - Vulnerability scan results
   - NSR security validation
   - Compliance status

### Downloading Artifacts

**GitHub UI**:
1. Open workflow run
2. Scroll to **Artifacts** section
3. Click artifact name to download

**GitHub CLI**:
```bash
# Download all artifacts from run
gh run download <run-id>

# Download specific artifact
gh run download <run-id> -n ipfs-deployment-report
```

## Accessing Deployments

### IPFS Gateway Access

Each deployment to main branch creates an IPFS deployment:

1. Find the IPFS hash in the deployment report
2. Access via gateway: `https://ipfs.io/ipfs/<IPFS_HASH>`
3. Replace `<IPFS_HASH>` with actual hash from report

**Example**:
```
https://ipfs.io/ipfs/QmXxxx...
```

### Finding Latest Deployment

```bash
# List recent deployments
gh run list --workflow=kosymbiosis-cd.yml --limit 1

# Get run ID and download report
gh run download <run-id> -n ipfs-deployment-report

# View the report
cat ipfs-deployment-report.md
```

## Common Tasks

### Check NSR Score

```bash
# Run CI workflow
gh workflow run kosymbiosis-ci.yml

# Wait for completion
gh run watch

# Download NSR report
gh run download --name nsr-validation-report

# View report
cat nsr-report.md
```

### Trigger Emergency Deployment

```bash
# Emergency deployment (faster, skips non-critical checks)
gh workflow run kosymbiosis-cd.yml -f deployment_type=emergency
```

### Force Klimabaum Sync

```bash
# Sync Klimabaum nodes without full deployment
gh workflow run kosymbiosis-cd.yml -f deployment_type=klimabaum-sync
```

### View Security Status

```bash
# Trigger security scan
gh workflow run kosymbiosis-security.yml

# Wait and download report
gh run watch
gh run download --name security-report

# View report
cat security-report.md
```

## Troubleshooting

### NSR Validation Failed

**Problem**: NSR score below 0.80

**Solution**:
1. Review NSR validation report
2. Check recent code changes
3. Ensure Lex Amoris compliance
4. Update documentation if needed
5. Re-run validation

### Deployment Failed

**Problem**: IPFS deployment or Klimabaum sync failed

**Solution**:
1. Check self-healing log
2. System automatically falls back to previous version
3. Review error details in deployment metrics
4. Re-trigger deployment if needed

### Security Scan Warnings

**Problem**: Security vulnerabilities detected

**Solution**:
1. Review security report
2. Update vulnerable dependencies
3. Fix identified issues
4. Re-run security scan

## Best Practices

1. **Always Review NSR Score**
   - Maintain score >= 0.80
   - Address violations immediately
   
2. **Monitor Deployments**
   - Check IPFS deployment reports
   - Verify Klimabaum sync status
   - Test gateway URLs
   
3. **Keep Documentation Updated**
   - System auto-updates documentation
   - Review changes for accuracy
   - Add manual updates as needed
   
4. **Security First**
   - Regular security scans
   - Update dependencies
   - Review security reports
   
5. **Use Artifacts**
   - Download important reports
   - Archive deployment metadata
   - Track NSR trends

## Getting Help

### Documentation

- [CI/CD Overview](CI-CD-OVERVIEW.md) - Comprehensive system documentation
- [Implementation Summary](IMPLEMENTATION-SUMMARY.md) - Technical details
- [Security Summary](SECURITY-SUMMARY.md) - Security information

### GitHub Issues

For problems or questions:
1. Create GitHub issue
2. Add `ci-cd` label
3. Include workflow run ID
4. Attach relevant artifacts

### Workflow Status Badges

Check README for current status:
- CI Status Badge
- CD Status Badge
- Documentation Badge
- Security Badge

## Advanced Usage

### Custom NSR Threshold

To modify NSR threshold (requires workflow edit):

```yaml
env:
  NSR_THRESHOLD: "0.85"  # Increase from 0.80
```

### Custom IPFS Gateway

To use different IPFS gateway:

```yaml
env:
  IPFS_GATEWAY: "https://your-gateway.io/ipfs"
```

### Additional Klimabaum Nodes

To add more anchor nodes:

```yaml
env:
  KLIMABAUM_NODES: "Yambio,Svalbard,Lantana,NewNode"
```

## Summary

The Kosymbiosis CI/CD system provides:
- ✅ Automated validation and deployment
- ✅ NSR and Lex Amoris compliance
- ✅ IPFS-based immutable deployments
- ✅ Self-healing capabilities
- ✅ Comprehensive logging and metrics

**Start using it**: Every push automatically triggers validation. Merge to main triggers deployment.

---

*Lex Amoris Signature: CI/CD guidance complete* 📚 ✅ ⚖️

**Last Updated**: 2026-02-12
