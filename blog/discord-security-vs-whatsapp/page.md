---
tags: security, privacy, foss
author: ONLIX
subtitle: Is Discord really more secure than WhatsApp? I compared them.
---

Thanks to PhotoMIX-Company on Pixabay for the [picture](https://pixabay.com/photos/monitoring-security-surveillance-1305045/).

# Discord's Security VS WhatsApp's
## Overview

<table>
    <thead>
        <tr>
            <th>Criteria</th>
            <th>Discord</th>
            <th>WhatsApp</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Ad-free</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td>You can request your data</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td>You can request a removal of your data</td>
            <td>❔¹</td>
            <td>✅</td>
        </tr>
        <tr>
            <td>Encrypted message content</td>
            <td>❌</td>
            <td>✅</td>
        </tr>
        <tr>
            <td>Service can't read private message content</td>
            <td>❌</td>
            <td>✅</td>
        </tr>
        <tr>
            <td>Service can't listen to voice calls</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
            <td>2FA/MFA</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td>Registration without phone</td>
            <td>✅</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>No collection of credit card info</td>
            <td>❌</td>
            <td>✅</td>
        </tr>
        <tr>
            <td>Independent from tech giants</td>
            <td>❔²</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>No third party tracking</td>
            <td>❌</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>Encrypted message metadata</td>
            <td>❌</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>Open Source</td>
            <td>❌</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>Decentralized</td>
            <td>❌</td>
            <td>❌</td>
        </tr>
        <tr>
            <td>Onion/Hidden Service</td>
            <td>❌</td>
            <td>❌</td>
        </tr>
        <tr>
            <td><i>ToS;DRos</i> Terms of Service Grade</td>
            <td><a href="https://tosdr.org/en/service/536" style="color: red;">E</td>
            <td><a href="https://tosdr.org/en/service/198" style="color: red;">E</td>
        </tr>
        <tr>
            <td><strong>Score</strong></td>
            <td>6</td>
            <td>8</td>
        </tr>
    </tbody>
</table>

¹ This one isn't fully clear. While for example Sony has some shares and other programming libraries from third party companies (e.g. *Twemoji*) are used, Discord is still more or less independent in general. Still, as this might change in the future, as we've seen with Elon Musk buying Twitter, sadly not a checkmark for Discord this time.

² Discord doesn't delete your messages. It changes your username in the pattern "Deleted User XYZ123456" which isn't making your account private at all (since you can often easily tell who that user was). Even the user's direct messages are still visible to the recipient (just the username & profile picture is changed). Because of these limitations, I don't think Discord deserves to get a checkmark for this criteria.

## Conclusion
Neither are really private & secure. WhatsApp claims it is, even though some of their practices are really questionable. I'd personally say **Discord is a bit less secure than WhatsApp**, but the best is to just avoid both of them if possible.

## Alternatives
The two alternatives I'm mentioned here pass almost all the criteria listed in the table above, so go check them out!

Use [Element (Matrix)](https://element.io/) instead of **Discord** - it's much safer as well as open source. Some people might say it's more like an alternative for Slack, but personally, I really think anyone who uses Discord will get used to it pretty quickly. It supports screen share, permissions, and much more, just like Discord does.

Want to have a Discord-like experience without having to get used to Element? Try [Revolt](https://revolt.chat)! It's a great privacy-focused and open source alternative. You can also self-host it, there is an API available and it's even accessible on F-Droid. It's still in beta, though and MacOS/iOS support is not yet available.

Use [Signal](https://signal.org) instead of **WhatsApp**. It's a great option for privacy and security. Just as Element for Discord, I think WhatsApp users shouldn't have that many problems switching to Signal. It has everything you need: voice messages, calls, notes and more. In addition to that, I'm really enjoying the theme options for Signal as well as the notes, a nice desktop client and a screen share feature. I'm unsure if I'd recommend the payment feature though - surely useful for basic stuff, but [Monero](https://www.getmonero.org/) is much safer from what I've heard.

Also, I wouldn't recommend using Element/Revolt as a replacement of WhatsApp if you want to keep things simple.
In the other hand, I also don't think Signal is a perfect replacement for Discord - it's just lacking in tons of advanced features such as permission management.

### Note
I've also heard about [Fosscord](https://fosscord.com/) as a Discord alternative, but as its development isn't completed yet and I'm unsure if it might get sued for using Discord's frontend or something, I can't really tell whether I'll use it or not.

Also, avoid [Guilded](https://www.guilded.gg/) because it has a bad [privacy rating]((https://tosdr.org/en/service/2646)) and it isn't fully open source.