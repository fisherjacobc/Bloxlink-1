from ..structures.Bloxlink import Bloxlink # pylint: disable=import-error, no-name-in-module
from ..constants import DEFAULTS # pylint: disable=import-error, no-name-in-module
from ..exceptions import CancelCommand, RobloxDown, Blacklisted # pylint: disable=import-error, no-name-in-module
import discord

get_guild_value = Bloxlink.get_module("cache", attrs=["get_guild_value"])
guild_obligations = Bloxlink.get_module("roblox", attrs=["guild_obligations"])


@Bloxlink.module
class MemberUpdateEvent(Bloxlink.Module):
    def __init__(self):
        pass

    async def __setup__(self):

        @Bloxlink.event
        async def on_member_update(before, after):
            guild = before.guild

            if guild.verification_level == discord.VerificationLevel.highest:
                return

            if not before.bot and (before.pending and not after.pending) and "COMMUNITY" in guild.features:
                options = await get_guild_value(guild, ["autoRoles", DEFAULTS.get("autoRoles")], ["autoVerification", DEFAULTS.get("autoVerification")], "highTrafficServer")

                auto_roles = options.get("autoRoles")
                auto_verification = options.get("autoVerification")
                high_traffic_server = options.get("highTrafficServer")

                if auto_verification or auto_roles:
                    try:
                        await guild_obligations(after, guild, roles=not high_traffic_server, nickname=not high_traffic_server, cache=False, join=True, dm=True, event=True, exceptions=("RobloxDown", "Blacklisted"))
                    except CancelCommand:
                        pass
                    except RobloxDown:
                        try:
                            await after.send("Roblox appears to be down, so I was unable to retrieve your Roblox information. Please try again later.")
                        except discord.errors.Forbidden:
                            pass
                    except Blacklisted as b:
                        pass
