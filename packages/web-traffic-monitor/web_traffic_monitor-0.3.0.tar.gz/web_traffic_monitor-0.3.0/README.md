# web_traffic_monitor
under construction

[Documentation](https://jameskabbes.github.io/web_traffic_monitor)<br>
[PyPI](https://pypi.org/project/kabbes-web-traffic-monitor)

# Usage

```python
import web_traffic_monitor
client = web_traffic_monitor.Client()
```

## Client functionality

### log_visit( slug, dt: defaults to current datetime )
Logs a visit for a given slug at a specified datetime. 

### get_active_redirect( slug )
Returns the active redirect for a given slug, or None if it doesn't exist.

### add_redirect( slug, redirect, dt: defaults to current time )
Deactives existing redirect for given slug, and adds a new redirect at given datetime.

### deactivate_redirect( slug, dt: defaults to current time )
Deactivates active redirect for a given slug, by specifying and END_DATETIME = dt

# Description
This repo serves a couple of basic purposes:
1. Logs visits to a webpage
2. Redirects slugs to new addresses

The functionality is pretty basic, and the most important piecs are contained in the database schema. A `DB` class (built for sqlite) is provided with the package. Feel free to overwrite the class functionality if you want to use your own database engine.

# Schema

## visits

| slug                     | datetime                 |
|--------------------------|--------------------------|
| /home                    | 2023-09-22 08:15:00+0000 |
| /about-us                | 2023-09-23 14:32:00+0000 |
| /contact                 | 2023-09-24 10:45:00+0000 |
| /products/latest-deals   | 2023-09-25 18:20:00+0000 |
| /blog/post-1             | 2023-09-26 09:10:00+0000 |
| /services                | 2023-09-27 12:55:00+0000 |
| /blog/post-2             | 2023-09-28 16:40:00+0000 |
| /portfolio/project-xyz   | 2023-09-29 11:25:00+0000 |
| /products/sale-items     | 2023-09-30 08:50:00+0000 |
| /blog/post-3             | 2023-10-01 13:05:00+0000 |

## redirects

| id    | slug           | redirect                | start_datetime           | end_datetime             |
|-------|----------------|-------------------------|--------------------------|--------------------------|
| 1     | /old-page      | /new-page1              | 2023-09-22 08:15:00+0000 | 2023-09-23 14:32:00+0000 |
| 2     | /old-page      | /new-page2              | 2023-09-23 14:32:00+0000 | 2023-09-24 10:45:00+0000 |
| 3     | /old-page      | /new-page3              | 2023-09-24 10:45:00+0000 |                          |
| 4     | /coming-soon   | /modern-version         | 2023-09-23 14:32:00+0000 | 2023-09-24 10:45:00+0000 |
| 5     | /coming-soon   | /modern-version2        | 2023-09-24 10:45:00+0000 |                          |
| 6     | /outdated-info | /updated-info           | 2023-09-25 18:20:00+0000 |                          |
| 7     | /contact-old   | /contact-new            | 2023-09-26 09:10:00+0000 |                          |
| 8     | /expired1      | /events/event-2021      | 2023-09-22 08:15:00+0000 | 2023-09-23 14:32:00+0000 |
| 9     | /expired2      | /new-offer              | 2023-09-23 14:32:00+0000 | 2023-09-24 10:45:00+0000 |
| 10    | /expired3      | /fallback-page          | 2023-09-24 10:45:00+0000 |                          |

# Author
James Kabbes