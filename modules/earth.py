import time
import colorama
import os

ascii_frames = [
    ''' 
                              _v->#H#P? "':o<>\_
                          .,dP` `''  "'-o.+H6&MMMHo_
                        oHMH9'         `?&bHMHMMMMMMHo.
                      oMP"' '           ooMP*#&HMMMMMMM?.
                    ,M*          -     `*MSdob//`^&##MMMH\\
                  d*'                .,MMMMMMH#o>#ooMMMMMb
                  HM-                :HMMMMMMMMMMMMMMM&HM[R\\
                d"Z\\.               9MMMMMMMMMMMMMMMMM[HMM|:
                -H    -              MMMMMMMMMMMMMMMMMMMbMP' :
                :??Mb#               `9MMMMMMMMMMMMMMMMMMH#! .
                : MMMMH#,              "*""`#HMMMMMMMMMMH  -
                ||MMMMMM6\\.                    {MMMMMMMMMH'  :
                :|MMMMMMMMMMHo                 `9MMMMMMMM'   .
                . HMMMMMMMMMMP'                 !MMMMMMMM    `
                - `#MMMMMMMMM                   HMMMMMMM*,/  :
                :  ?MMMMMMMF                   HMMMMMM',P' :
                  .  HMMMMR'                    {MMMMP' ^' -
                  : `HMMMT                     iMMH'     .'
                    -.`HMH                               .
                      -:*H                            . '
                        -`\\,,    .                  .-
                          ' .  _                 .-`
                              '`~\\.__,obb#q==~
    '''
    , 
    ''' 
                              .ovr:HMM#?:`' >b\\_
                          .,:&Hi' `'   "' \\\|&bSMHo_
                        oHMMM#*}          `?&dMMMMMMHo.
                    .dMMMH"''           ,oHH*&&9MMMM?.
                    MMM*'                 `*M\\bd<|"*&#MH\\
                  dHH?'                   :MMMMMM#bd#odMML
                  H' |\\                  `dMMMMMMMMMMMMMM9Mk
                JL/"7+,                `MMMMMMMMMMMMMMMH9ML
                -`Hp     '               |MMMMMMMMMMMMMMMMHH|:
                :  \\#M#d?                `HMMMMMMMMMMMMMMMMH.
                .   JMMMMM##,              ``*""'"*#MMMMMMMMH
                -. ,MMMMMMMM6o_                    |MMMMMMMM':
                :  |MMMMMMMMMMMMMb\\                 TMMMMMMT :
                .   ?MMMMMMMMMMMMM'                 :MMMMMM|.`
                -    ?HMMMMMMMMMM:                  HMMMMMM\\|:
                :     9MMMMMMMMH'                 `MMMMMP.P.
                  .    `MMMMMMT''                   HMMM*''-
                  -    TMMMMM'                     MM*'  -
                    '.   HMM#                            -
                      -. `9M:                          .'
                        -. `b,,    .                . '
                          '-\\   .,               .-`
                              '-:b~\\\\_,oddq==--"
    '''
    ,
    ''' 
                              _oo##'9MMHb':'-,o_
                          .oH":HH$' ""'  "' -\\7*R&o_
                      .oHMMMHMH#9:          "\\bMMMMHo.
                      dMMMMMM*""'`'           .oHM"H9MM?.
                    ,MMMMMM'                   "HLbd<|?&H\\
                  JMMH#H'                     |MMMMM#b>bHb
                  :MH  ."\                   `|MMMMMMMMMMMM&
                .:M:d-"|:b..                 9MMMMMMMMMMMMM+
                :  "*H|      -                &MMMMMMMMMMMMMH:
                .    `LvdHH#d?                `?MMMMMMMMMMMMMb
                :      iMMMMMMH#b               `"*"'"#HMMMMMM
                .   . ,MMMMMMMMMMb\\\.                   {MMMM
                -     |MMMMMMMMMMMMMMHb,               `MMMMM|
                :      |MMMMMMMMMMMMMMH'                &MMMM,
                -       `#MMMMMMMMMMMM                 |MMMM6-
                :        `MMMMMMMMMM+                 ]MMMT/
                  .       `MMMMMMMP"                   HMM*`
                  -       |MMMMMH'                   ,M#'-
                    '.     :MMMH|                       .-
                      .     |MM                        -
                      ` .   `#?..    .             ..'
                          -.     _.             .-
                              '-|.#qo__,,ob=~~-''

    '''
    ,
    ''' 
                              _ooppH[`MMMD::--\\_
                          .\\HMMMMMR?`\\M6b."`' ''``v.
                      .. .MMMMMMMMMMHMMM#&.      ``~o.
                    .   ,HMMMMMMMMMMMM*"'-`          &b.
                    .   .MMMMMMMMMMMMH'               `"&\\
                  -     RMMMMM#H##R'                   4Mb
                  -      |7MMM'    ?::                 `|MMb
                /         HMM__#|`"\\>?v..              `MMML
                .           `"'#Hd|       `              9MMM:
                -                |\\,\\?HH#bbL             `9M
                :                   !MMMMMMMH#b,          `""T
                .              .   ,MMMMMMMMMMMbo.           |
                :                  4MMMMMMMMMMMMMMMHo        |
                :                   ?MMMMMMMMMMMMMMM?        :
                -.                   `#MMMMMMMMMMMM:        .-
                :                     |MMMMMMMMMM?         .
                  -                    JMMMMMMMT'          :
                  `.                   MMMMMMH'           -
                    -.                |MMM#*`            -
                      .               HMH'            . '
                        -.            #H:.          .-
                          ` .           .\\       .-
                              '-..-+oodHL_,--/-`

    '''
    ,
    ''' 
                              _,\\?dZkMHF&$*q#b..
                          .//9MMMMMMM?:'HM\\"`-''`..
                      ..`  :MMMMMMMMMMHMMMMH?_    `-\\.
                    .     .dMMMMMMMMMMMMMM'"'"       `\\.
                    .      |MMMMMMMMMMMMMR              \\\\
                  -        T9MMMMMHH##M"                `?
                  :          (9MMM'    !':.               &k
                .:            HMM\\_?p "":-b\\.            `ML
                -                "'"H&#,       :           |M|
                :                     ?\\,\\dMH#b#.           9b
                :                        |MMMMMMM##,        `*
                :                   .   +MMMMMMMMMMMo_       -
                :                       HMMMMMMMMMMMMMM#,    :
                :                        9MMMMMMMMMMMMMH'    .
                : .                       *HMMMMMMMMMMP     .'
                :                          MMMMMMMMMH'     .
                  -                        :MMMMMMM'`      .
                  `.                       9MMMMM*'       -
                    -.                    {MMM#'         :
                      -                  |MM"          .'
                      `.                &M'..  .   ..'
                          ' .             ._     .-
                              '-. -voboo#&:,-.-`

    ''',
    """

                              _o,:o?\?dM&MHcc~,.
                          ..^':&#""HMMMMMMMM$:?&&?.
                        .`  -`      'HMMMMMMMMMHMMMp\.
                    . '             |MMMMMMMMMMMMMM"' .
                    .                `9MMMMMMMMMMMMM    -.
                  -                   `*9MMMMMHH##[      .
                  -                     `\Z9MMM    `~\     .
                :       '|                 ?MMb_?p""-?v..  :
                -                             `"'*&#,    -   .
                :                                  `?,oHH#?  .
                --                                    |MMMMH,:
                :                                 .  |MMMMMM6,
                :   -                                |MMMMMMMM
                ?                                     HMMMMMMP
                -- . '                                |HMMMMM'
                :.`     .  '                          JMMMM+
                  \                                   ,MMMP:
                  :                                 |MMH?:
                    -:\.                            dM#" .
                      \                          ,H*' .'
                        -.                       d':..'
                          ` .                  .,.-
                              '-.. .\oooodov~^-`

    """,
    """
                              _o\:,??\??MR9#cb\_
                          .v/''':&#""#HMMMMMMM$?*d\.
                      ..~' - -`      `"#MMMMMMMMMMMHv.
                    .-'                 HMMMMMMMMMMMR!.
                    :                    `9MMMMMMMMMMM| -.
                  .                       `*9MMMMMH##|   .
                  -                          `(#MMH   `:,  .
                :           '|                 `HMb_>/"|\,.:
                .'                                `"'#&b   - .
                :                                      ?\oHH?.
                :                                        !MMM&
                :  .                                  .  HMMMM
                /.      -                               -MMMMM
                \`.                                      9MMMP
                :. .  . -                                |MMM'
                \... '                                  .MMT
                  &.                                    .dMP
                  \,                                  .HM*
                    \. `\.                            ,H&'
                    `- `| -                        ,&':
                      `.                         ,/\ '
                          '-..                  _.-
                              "---.._\o,oov+--'"
    """,
    """
                              ,d?,:?o?:?HM>#b\_
                          ..H*"''`'H#*"**MMMMMM6$$v_
                        v//"   - ``      `'#MMMMMMMMHo.
                      /"`                   |MMMMMMMMMM:.
                    ,>                       `HMMMMMMMMH:.
                  :                           `#HMMMMHH\ -
                  '                              `Z#MM,  `,:
                :               '\                 ?HH_>:`\,
                :                                     "'*&| `:
                .                                         <\Hb
                :                                           MM
                :                                        . iMM
                Mb\.                                       {MM
                ::.`-       -                              !MP
                `&.   .  .  -                              :M'
                9H,  \  '                                 |T
                  HM?                                     ,P
                  *ML                                   ??
                    :&.   `o                           .d'
                      ':  |T                          /"
                        -.                         .<''
                          `...                  ..-
                              "`-=.,_,,,oov-~.-`
    """,
    """
                              _,oc>?_:b?o?HH#b\_
                          .v/99*"" '*H#""*HMMMMMZ,_
                        oH* /"   -   '      "`#MMMMM#o.
                    ./*>-                     `MMMMMMMb
                    ,b/'                        `#MMMMMMM\
                  :'                             ``HMMMMb:
                  /-                                `|&MH `\
                /                   `-.               |Hb??\
                ,-  '                                    "`&,.
                1                                           \}
                !.                                           T
                $,.                                        . 1
                ?`M??.                                       M
                ?.::| '\        -                            ?
                M?&.    .   .  -                           ,'
                9MMH\   ..  '           `                  .
                  HMMM#.                                   :'
                  9#MMb                                 ..
                    -:"#     `b.                        .-
                      . `    {!                        /
                        -                           ,-'
                          ' .                    .-
                            ```^==\_.,,,ov--\-`
    """,
    """
                              _\o##??,:io??$#b\_
                          .oH#"H9*"" "`#H*"*#MMMHo_
                        oHMM- -'    -  ''     ``*HMMHo.
                    .dMMM#">>-                     `HM?.
                    ,&&,/'                         "#MMMH\
                  d?-"                              `*HMMb
                  H?                                   "ZHb:
                /:                        \              H?L
                |:|   .                                    `*:
                :?:                                          \
                >"                                           :
                M|\,_                                        |
                !|":HH?-'.                                   :
                :^'_:?"\ `--         -                       .
                - |ML?b      .   ..  -                       -
                :HMMMMH\    \               `              :
                  >MMMMMM#.                                .
                  ^M*HMMM|                               -
                    `. `"#+     `?v                     .`
                      .   `-    +?'                    -
                      ` .                          ..'
                          - .                   .-
                              ```*##dMMo.\vv----`
    """,
    """
                              _,o#bH\??::?o?cbo_
                          .o#MH#**SH""' "`*H#"*#MHo_
                        oHMMMH^  ^"    -  `      '*HHo.
                    .dMMM#">>-                     `HM?.
                    ,MH:R_o/                         `*MH\
                  dMM' '                               "ML
                  HMR! '                                 `#k
                d&'.                          -.          `L
                :M ::     `                                 `-
                /| !|                                        -
                k.$-"                                        :
                }9R:!,,_.                                    .
                \::\':`*M#\-'.                               -
                : "''..:"!`\  '-          -                  `
                -   ,HMb.H|      .    _   -                 .'
                : ,MMMMMMMb.    ..                         .
                  .`HMMMMMMMM?                             .
                  `.`9M#*HMMMM                            :
                    -.'   "##*      `b,                  .
                      .      `     ,/'                 .'
                      ` .                          ..'
                          - .                  ..-
                              "`*##d##c.._\v----`
    """,
    """
                              _,o#&oHb?\o::d?>\_
                          .oHHMMM#**$M""` "`*HH"#&o_
                        oHMMMMMMD' .''    -  '    ``bo.
                    .dMMMMMH*'/|-                   `\b.
                    ,MMMM?T|_o/                        `\\
                  dMMM' '                               "|
                  HMMMH& -                                `\
                /MH7' :                          --        :
                -:MM  {.      .                              .
                :i?' .!&                                     .
                :{, o| '                                     :
                -T?9M\:-'o,_                                 .
                : \?::``"`?9MHo./..                          -
                .  '"`'^ _.`"!"^.  `-         -              `
                -      ,bMM?.M\       .    .  -      .      .'
                :   .oMMMMMMMMb.    ..   `                 .
                  .  `HMMMMMMMMMMb                         -
                  -   9MH*#HMMMMH                        .'
                    '.  '   `"*##'      `b.              :
                      .         `     .d''             .'
                        -.                          . '
                          -.                    .-`
                              "`*#d##c.._\v----`
    """,
    """
                                  _o,d_?dZdoHHHb#b\_
                          .vdMMMMMMMMMMMMMMMMMMMMH\.
                      .,HHMMMMMMMMMMMMMMMMMMMMMMMMH&,.
                      /?RMMMMMMMMMMMMMMMMMMMMMMMMMMMMH|..
                    ,\?>`T#RMMMMMMMMMMMMMMMMMMMMMMMM6`\|/
                  dMMbd#ooHMMMHMMMMMMMMMMMMMMMMMMMMMH,`' '
                  HMMMMMMMTMMMMb$ZP**HMMMMMMMMMMMMMMMM|.   :
                dMMMMMMMM}$MMMMMH'   `HMMMH?"`MMMM?T' .    :
                |MMMMMMMMMMoMH*''      `MM?    ``MMM|  +\    .
                1MMMMMMMMMMMb#/         ?#?      |`#"  -T:   :
                *'HMMMMMMMMMM*'           "     ~?&  .?} ' ' .
                - 4MMMMMMMMP"                    `M? HMTc:\\.:
                : `MMMMMMM[                       "#:::`>`"?M{
                .  |MMMMMMH.                        ``'``'_`:-
                -  |MMMMMMM|.dD                         ,#Mb\'
                :  *MMMMM: iM|  .                   _oHMMMM:
                  .  ?MMMM'  "'                     ,MMMMMMP
                  :  `HMH                          JM#*MMT
                    -.  '                           `   #'
                      .                                /
                        -.            -              .'
                          -.                    . `
                              '--=&&MH##HMHH#""
    """,
]


def rotate_ascii_art(frames, delay=0.1):
    for frame in range(len(frames)):
        print(colorama.Fore.GREEN+frames[frame], end='\r', flush=True)
        time.sleep(delay)
    for frame in range(-len(frames),0):
        print(frames[frame], end='\r', flush=True)
        time.sleep(delay)

def Earth():
    rotate_ascii_art(ascii_frames)
    os.system("clear")
    print(colorama.Fore.GREEN+ascii_frames[0], end='\r', flush=True)