#!/bin/bash
# Configure COPR packages to use rpmautospec with git SCM

COPR_OWNER="makirill"
COPR_PROJECT="hyprwm"
GIT_URL="https://github.com/kmalgich/hyprwm-copr.git"  # Update this with your actual git URL

# List of packages to configure
PACKAGES=(
    "aquamarine"
    "glaze"
    "hyprcursor"
    "hyprgraphics"
    "hypridle"
    "hyprland"
    "hyprland-guiutils"
    "hyprland-protocols"
    "hyprlang"
    "hyprlock"
    "hyprpaper"
    "hyprtoolkit"
    "hyprutils"
    "hyprwayland-scanner"
    "hyprwire"
    "uwsm"
    "xdg-desktop-portal-hyprland"
)

echo "This script will configure COPR packages to use rpmautospec"
echo "COPR Project: $COPR_OWNER/$COPR_PROJECT"
echo "Git URL: $GIT_URL"
echo ""
echo "Prerequisites:"
echo "  - Install copr-cli: sudo dnf install copr-cli"
echo "  - Configure API token: copr-cli --help"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

for package in "${PACKAGES[@]}"; do
    echo ""
    echo "==================================="
    echo "Configuring: $package"
    echo "==================================="

    # Edit package to use SCM source with rpmautospec
    copr-cli edit-package-scm \
        --clone-url "$GIT_URL" \
        --commit main \
        --subdir "$package" \
        --spec "$package.spec" \
        --type git \
        --method rpkg \
        "$COPR_OWNER/$COPR_PROJECT" \
        --name "$package" \
        --webhook-rebuild on

    if [ $? -eq 0 ]; then
        echo "✓ Successfully configured $package"
    else
        echo "✗ Failed to configure $package"
    fi
done

echo ""
echo "==================================="
echo "Configuration complete!"
echo "==================================="
echo ""
echo "Now test with one package:"
echo "  1. Make a change to a spec file (e.g., uwsm/uwsm.spec)"
echo "  2. Commit: git commit -am 'Test build'"
echo "  3. Push: git push"
echo "  4. Rebuild: copr-cli build-package $COPR_OWNER/$COPR_PROJECT --name uwsm"
