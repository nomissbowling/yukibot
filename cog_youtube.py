import pathlib
import subprocess
import tempfile

import discord
from discord.ext import commands


class YouTube(commands.Cog):

    @commands.command(usage='<動画ソース> [再生を開始する秒数] [再生する秒数]', help='動画を再生します。 例: /playback "youtu.be/TQ8WlA2GXbk" 1:33 0:12', aliases=['play', 'p', 'p5'])
    async def playback(self, ctx, video_src, start_time: str = '0:00', duration_time: str = '0:30'):
        sel_entry = ['bestvideo[height<=360][ext=webm]+bestaudio[ext=webm]',
                     'bestvideo[height<=360]+bestaudio',
                     'best[ext=webm][height<=360]',
                     'best[height<=360]',
                     'best']

        cmd1 = ['youtube-dl',
                '-f', '/'.join(sel_entry),
                '--get-filename',
                video_src]

        x = await ctx.send(f'ファイル名を検証しています...\n{cmd1}')
        filename = subprocess.check_output(cmd1).decode().rstrip()

        p = pathlib.Path(filename)
        tmp1 = pathlib.Path(tempfile.NamedTemporaryFile(suffix=p.suffix).name)
        tmp2 = tmp1.parent / f'{tmp1.stem}-cropped{p.suffix}'

        cmd2 = ['youtube-dl',
                '-f', '/'.join(sel_entry),
                '-o', tmp1,
                video_src]

        cmd3 = ['ffmpeg',
                '-ss', start_time,
                '-i', tmp1,
                '-t', duration_time,
                '-c', 'copy',
                tmp2]

        await x.edit(content=f'ダウンロードを実行しています...\n{cmd2}')
        subprocess.check_call(cmd2)

        await x.edit(content=f'変換しています...\n{cmd3}')
        subprocess.check_call(cmd3)

        await x.delete()

        upload = discord.File(tmp2)
        await ctx.send(file=upload)
