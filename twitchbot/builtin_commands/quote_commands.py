import re

from twitchbot import (
    Command,
    Message,
    delete_quote_by_id,
    add_quote,
    get_quote_by_alias,
    get_quote,
    Quote,
    cfg,
    InvalidArgumentsException)

PREFIX = cfg.prefix


@Command('addquote', syntax='"<quote text>" user=(user) alias=(alias)', help='adds a quote to the database')
async def cmd_quote_add(msg: Message, *args):
    if not args:
        raise InvalidArgumentsException()

    optionals = ' '.join(args[1:])

    user = alias = None
    if 'user=' in optionals:
        m = re.search(r'user=(\w+)', msg.content)
        if not m:
            await msg.reply('invalid user')
            return

        user = m.group(1)

    if 'alias=' in optionals:
        m = re.search('alias=(\w+)', msg.content)
        if not m:
            await msg.reply('invalid alias')
            return

        alias = m.group(1)
        if get_quote_by_alias(msg.channel_name, alias) is not None:
            await msg.reply('there is already a quote with that alias')
            return

    if add_quote(Quote.create(channel=msg.channel_name, value=args[0], user=user, alias=alias)):
        resp = 'successfully added quote'
    else:
        resp = 'failed to add quote, already exist'

    await msg.reply(resp)


@Command('quote', syntax='<ID or ALIAS>', help='gets a quote by ID or ALIAS')
async def cmd_get_quote(msg: Message, *args):
    if not args:
        raise InvalidArgumentsException()

    quote = get_quote(msg.channel_name, args[0])
    if quote is None:
        await msg.reply(f'no quote found')
        return

    await msg.reply(f'"{quote.value}" user: {quote.user} alias: {quote.alias}')


@Command('delquote', permission='delete_quote', syntax='<ID or ALIAS>', help='deletes the quote from the database')
async def cmd_del_quote(msg: Message, *args):
    if not args:
        raise InvalidArgumentsException()

    quote = get_quote(msg.channel_name, args[0])
    if quote is None:
        await msg.reply(f'no quote found')
        return

    delete_quote_by_id(msg.channel_name, quote.id)

    await msg.reply(f'successfully deleted quote, id: {quote.id}, alias: {quote.alias}')
