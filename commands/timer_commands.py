from command import Command
from message import Message
from database import (
    set_message_timer_active,
    set_message_timer_interval,
    set_message_timer_message,
    set_message_timer,
    message_timer_exist,
    delete_message_timer,
    delete_all_message_timers,
    get_all_channel_timers,
    get_message_timer
)
from config import cfg

PREFIX = cfg.prefix
MIN_MESSAGE_TIMER_INTERVAL = 10


async def _parse_interval(msg, value):
    try:
        interval = float(value)
        if interval < MIN_MESSAGE_TIMER_INTERVAL:
            raise ValueError()
        return True, value
    except ValueError:
        await msg.reply('invalid interval, must be a valid float and be above 10')
        return False, 0


@Command('addtimer')
async def cmd_add_timer(msg: Message, *args):
    if len(args) < 3:
        await msg.reply(f'invalid args: {PREFIX}addtimer <name> <interval> <message>')
        return

    valid, interval = await _parse_interval(msg, args[1])
    if not valid:
        return

    timer_msg = ' '.join(args[2:])
    timer_name = args[0].lower()

    if message_timer_exist(msg.channel_name, timer_name):
        await msg.reply(f'a timer already exist by the name of "{timer_name}"')
        return

    set_message_timer(msg.channel_name, timer_name, timer_msg, interval)

    await msg.reply(f'created timer successfully')


@Command('starttimer')
async def cmd_start_timer(msg: Message, *args):
    if not args:
        await msg.reply(f'invalid args: {PREFIX}starttimer <name>')
        return

    name = args[0]
    timer = get_message_timer(msg.channel_name, name)

    if not timer:
        await msg.reply(f'no timer was found by "{name}"')
        return

    if timer.running:
        await msg.reply(f'timer "{name}" is already running')
        return

    if set_message_timer_active(msg.channel_name, name, True):
        await msg.reply(f'successfully started the timer "{name}"')
    else:
        await msg.reply(f'failed to start the timer "{name}"')


@Command('stoptimer')
async def cmd_start_timer(msg: Message, *args):
    if not args:
        await msg.reply(f'invalid args: {PREFIX}stoptimer <name>')
        return

    name = args[0]
    timer = get_message_timer(msg.channel_name, name)

    if not timer:
        await msg.reply(f'no timer was found by "{name}"')
        return

    if not timer.running:
        await msg.reply(f'that timer is not running')
        return

    if set_message_timer_active(msg.channel_name, name, False):
        await msg.reply(f'successfully stopped the timer "{name}"')
    else:
        await msg.reply(f'failed to stop the timer "{name}"')


@Command('deltimer')
async def cmd_del_timer(msg: Message, *args):
    if not args:
        await msg.reply(f'invalid args: {PREFIX}deltimer <name>')
        return

    name = args[0]
    timer = get_message_timer(msg.channel_name, name)

    if not timer:
        await msg.reply(f'no timer was found by "{name}"')

    if delete_message_timer(msg.channel_name, name):
        await msg.reply(f'successfully deleted timer "{name}"')
    else:
        await msg.reply(f'failed to delete timer "{name}"')


@Command('listtimers')
async def cmd_list_timers(msg: Message, *args):
    timers = get_all_channel_timers(msg.channel_name)
    active_timers = ', '.join(timer.name for timer in timers if timer.active)
    inactive_timers = ', '.join(timer.name for timer in timers if not timer.active)

    if not active_timers and not inactive_timers:
        await msg.reply(f'no timers found for this channel')
        return

    if active_timers:
        await msg.reply(f'active timers: {active_timers}')

    if inactive_timers:
        await msg.reply(f'inactive timers: {inactive_timers}')