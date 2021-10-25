"""Plugin declaration for nautobot_plugin_chatops_aci."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import PluginConfig


class NautobotPluginChatopsAciConfig(PluginConfig):
    """Plugin configuration for the nautobot_plugin_chatops_aci plugin."""

    name = "nautobot_plugin_chatops_aci"
    verbose_name = "Nautobot Plugin Chatops Cisco ACI"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot Plugin Chatops Cisco ACI."
    required_settings = []
    min_version = "1.0.1"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = NautobotPluginChatopsAciConfig  # pylint:disable=invalid-name
