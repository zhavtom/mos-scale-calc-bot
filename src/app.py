import io
import os
from discord import File
from discord.ext import commands
import csv

TOKEN = os.environ["MOS_CALC_BOT_TOKEN"]

csv_path = "data/temp.csv"

bot = commands.Bot(command_prefix="m.")

async def on_ready():
    print("bot ready")

@bot.command()
async def calc(ctx, edo="", tonics="7", limit="8", export=""):

    result = []

    c = int(tonics)
    d = int(edo)
    
    lim = int(limit)
    if c == 0 or c > d or d == 0:
        raise commands.BadArgument()
        return

    for i in range(c//2):
        a = i + 1
        b = c - a
        x = 0
        while True:
            x += 1
            if x > d:
                break
            y = (d - a*x) / b
            ratio = y/x
            if y.is_integer() and y > 0 and ratio < lim and ratio > 1/lim:
                result.append([a, b, x, int(y)])

    output = "{} tonics, {}EDO の計算結果:\n```\n| a | b | x | y |\n|---|---|---|---|\n".format(tonics, edo)
    for row in result:
        for col in row:
            output += "|{:3}".format(col)
        output += "|\n|---|---|---|---|\n"
    output += "```"

    if len(output) > 2000:
        await ctx.send("文字数制限のため、csvファイルのみ出力します。")
        export = "csv"
    else:
        await ctx.send(output)
    
    if export == "csv":
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["a", "b", "x", "y"])
        writer.writerows(result)
        await ctx.send(file=File(io.BytesIO(buffer.getvalue().encode("utf-8")), "mos_{}tonics_{}edo.csv".format(tonics, edo)))


async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("引数を確認してください。")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("そのコマンドは存在しません。")


bot.add_listener(on_ready)
bot.add_listener(on_command_error)
bot.run(TOKEN)