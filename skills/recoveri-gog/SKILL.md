---
name: recoveri-gog
version: 1.0
description: Structured reference for invoking gog CLI commands. Gmail, Calendar, Drive for alfred@recoveri.io.
trigger: email|gmail|calendar|event|drive|upload|download|send email|draft|schedule|google
---

# Recoveri gog Skill v1.0

gog CLI provides authenticated access to Google services for alfred@recoveri.io.
Binary: /usr/local/bin/gog | Version: v0.11.0-176-gf40b348

## ENVIRONMENT SETUP

Export before every gog session:

  export GOG_KEYRING_PASSWORD=S2w74E8yahz6QKsYDhRMJg9tYf6s4_nQgIx3x7veq54
  export GOG_ACCOUNT=alfred@recoveri.io

Or inline prefix: GOG_KEYRING_PASSWORD=... GOG_ACCOUNT=alfred@recoveri.io gog <command>

## CRITICAL RULES

1. Run the actual command. Do not simulate or fabricate gog output.
2. Post raw output. Copy/paste real terminal output. Never paraphrase.
3. If a command fails, report the exact error. Never claim success without evidence.
4. Every file op must return a real Drive link via: gog drive get <fileId>
5. Never construct Drive URLs from memory. Build from confirmed fileId in gog output.
6. All syntax VERIFIED against live gog --help output on 2026-03-18.

## Gmail Operations

### Search / list recent emails (threads)

  gog gmail search "in:inbox" --max 10
  gog gmail search "from:someone@example.com subject:meeting" --max 10
  gog gmail search "is:unread" --max 20
  gog gmail search "in:inbox" --max 10 --json

Note: gog gmail search searches threads. Aliases: find, query, ls, list.

### Search messages (not threads)

  gog gmail messages search "in:inbox" --max 10

### Read a specific message

  gog gmail get MSG_ID
  gog gmail get MSG_ID --format metadata
  gog gmail get MSG_ID --json

Note: gog gmail get is a direct subcommand. Aliases: info, show.

### Download an attachment

  gog gmail attachment MSG_ID ATTACHMENT_ID

### Create a draft (do NOT send without Boss approval)

  gog gmail drafts create --to recipient@example.com --subject SUBJECT --body BODY
  gog gmail drafts create --to r@e.io --cc cc@e.io --subject SUBJECT --body BODY
  gog gmail drafts create --to r@e.io --subject SUBJECT --body BODY --reply-to-message-id MSG_ID

### List drafts

  gog gmail drafts list

### Send an email (Tier 3 - requires Boss approval via Neo)

  gog gmail send --to recipient@example.com --subject SUBJECT --body BODY
  gog gmail send --to r@e.io --subject SUBJECT --body BODY --attach /path/to/file
  gog gmail send --to r@e.io --subject SUBJECT --body BODY --thread-id THREAD_ID

### Send a saved draft

  gog gmail drafts send DRAFT_ID

### List labels

  gog gmail labels list

### Archive / mark read / unread

  gog gmail archive MSG_ID
  gog gmail mark-read MSG_ID
  gog gmail unread MSG_ID

## Calendar Operations

### List upcoming events

  gog calendar events --max 10
  gog calendar events --from 2026-03-18 --to 2026-03-25 --max 20
  gog calendar events --today
  gog calendar events --week
  gog calendar events --days 7
  gog calendar events alfred@recoveri.io --max 10
  gog calendar events --max 10 --json

Note: calendarId argument is optional (defaults to primary). Aliases: list, ls.

### Get a specific event

  gog calendar event primary EVENT_ID

Note: event (singular) aliases: get, info, show.

### Create an event

  gog calendar create primary --summary TITLE --from 2026-03-20T10:00:00+00:00 --to 2026-03-20T11:00:00+00:00
  gog calendar create primary --summary TITLE --from DATE_TIME --to DATE_TIME --attendees a@e.io,b@e.io
  gog calendar create primary --summary TITLE --from DATE_TIME --to DATE_TIME --with-meet
  gog calendar create primary --summary TITLE --from DATE_ONLY --to DATE_ONLY --all-day

IMPORTANT:
- First positional arg is calendarId. Use: primary
- Use --from / --to (NOT --start / --end -- those flags do NOT exist in this version)
- RFC3339 with timezone: 2026-03-20T10:00:00+00:00 (UTC) or +01:00 (BST)
- Default timezone context: Europe/London

### Update an event

  gog calendar update primary EVENT_ID --summary NEW_TITLE
  gog calendar update primary EVENT_ID --from DATE_TIME --to DATE_TIME

### Delete an event

  gog calendar delete primary EVENT_ID
  gog calendar delete primary EVENT_ID --force

IMPORTANT: --event-id flag does NOT exist. Both calendarId and eventId are positional.

### Search events

  gog calendar search "quarterly review" --max 10

### List calendars

  gog calendar calendars

### Check free/busy

  gog calendar freebusy primary --from DATE_TIME --to DATE_TIME

## Drive Operations

### List files

  gog drive ls
  gog drive ls --max 50
  gog drive ls --parent FOLDER_ID
  gog drive ls --json

Note: gog drive ls does NOT accept a positional folder name. Use --parent FOLDER_ID.

### Search Drive

  gog drive search "quarterly report"
  gog drive search "quarterly report" --max 20

### Get file metadata

  gog drive get FILE_ID
  gog drive get FILE_ID --json

Build shareable link: https://drive.google.com/file/d/FILE_ID/view?usp=sharing

### Upload a file

  gog drive upload /local/path/file.txt
  gog drive upload /local/path/file.txt --parent FOLDER_ID
  gog drive upload /local/path/file.txt --name custom-name.txt --parent FOLDER_ID
  gog drive upload /local/path/file.docx --convert --parent FOLDER_ID
  gog drive upload /local/path/file.txt --replace EXISTING_FILE_ID

Note: --parent takes a folder ID (not a name). Find IDs via gog drive ls or gog drive search.

### Download a file

  gog drive download FILE_ID
  gog drive download FILE_ID --out /local/output.txt
  gog drive download FILE_ID --format pdf --out /local/output.pdf
  gog drive download FILE_ID --format md --out /local/output.md

Note: correct flag is --out (NOT --output).

### Create a folder

  gog drive mkdir FolderName
  gog drive mkdir FolderName --parent PARENT_FOLDER_ID

### Other Drive operations

  gog drive url FILE_ID
  gog drive copy FILE_ID NewFileName
  gog drive move FILE_ID --parent DEST_FOLDER_ID
  gog drive rename FILE_ID NewName

## Drive Folder Map (reference)

Find current IDs: gog drive ls  or  gog drive search "folder-name"

Folder                   Purpose
00_Governance            Constitution, frameworks, policies
01_Sprints               Sprint backlogs, closeouts
02_Architecture          System design, technical architecture
03_Offers_and_Products   Product content, listings, value props
04_Research              Market research, intelligence briefs
05_Finance               Financial models, budgets
06_Experiments           Prototypes, test results
07_Content               Marketing, social media, brand
08_Operations            Process docs, SOPs
09_Security              Security reviews, audits
10_People                Team config, agent SOULs
77_Templates             Reusable templates
99_CEO                   Boss curated folder

## Error Handling

If gog returns an error:
1. Record the exact error message
2. Check: is GOG_KEYRING_PASSWORD set? Run: echo $GOG_KEYRING_PASSWORD
3. Check: is auth valid? (gog auth status)
4. If auth expired: escalate to Boss via Neo - do not attempt re-auth
5. Log to /root/error-register/ with error_type: tool_error

## Common Patterns

### Find and read a specific email

  gog gmail search "subject:invoice from:supplier@example.com" --max 5 --json
  gog gmail get MSG_ID --json

### Upload a file and get its Drive link

  gog drive upload /path/to/file.pdf --parent FOLDER_ID --json
  gog drive url FILE_ID
  # Build: https://drive.google.com/file/d/FILE_ID/view?usp=sharing

### Create a calendar event with Meet and attendee notifications

  gog calendar create primary --summary TITLE --from DATE_TIME --to DATE_TIME --attendees a@e.io,b@e.io --send-updates all --with-meet

