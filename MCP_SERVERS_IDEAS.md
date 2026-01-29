# MCP Servers You Can Build

Here's a comprehensive list of MCP servers you can build and use with your agent, organized by category.

## 📁 File & Document Operations

### 1. **File Manager MCP Server**
**Tools:**
- `read_file(path)` - Read file contents
- `write_file(path, content)` - Write/create files
- `list_directory(path)` - List files in directory
- `delete_file(path)` - Delete files
- `search_files(query, directory)` - Search for files by name/content

**Use Cases:** Document management, code editing, file organization

### 2. **PDF Operations MCP Server**
**Tools:**
- `extract_text_from_pdf(path)` - Extract text from PDF
- `merge_pdfs(files, output)` - Merge multiple PDFs
- `split_pdf(path, pages)` - Split PDF into pages
- `pdf_to_images(path)` - Convert PDF pages to images

**Use Cases:** Document processing, report generation

### 3. **Image Processing MCP Server**
**Tools:**
- `resize_image(path, width, height)` - Resize images
- `convert_image_format(path, format)` - Convert between formats
- `apply_filter(image, filter_type)` - Apply filters
- `extract_text_from_image(path)` - OCR text extraction

**Use Cases:** Image manipulation, OCR, format conversion

---

## 🌐 Web & API Integration

### 4. **Web Scraper MCP Server**
**Tools:**
- `fetch_url(url)` - Fetch webpage content
- `scrape_links(url)` - Extract all links
- `extract_text(url)` - Extract clean text
- `screenshot_url(url)` - Take screenshot

**Use Cases:** Web research, content extraction, monitoring

### 5. **REST API Client MCP Server**
**Tools:**
- `api_get(endpoint, headers)` - GET request
- `api_post(endpoint, data, headers)` - POST request
- `api_put(endpoint, data, headers)` - PUT request
- `api_delete(endpoint, headers)` - DELETE request

**Use Cases:** API integration, webhook handling

### 6. **Weather MCP Server**
**Tools:**
- `get_current_weather(location)` - Current weather
- `get_forecast(location, days)` - Weather forecast
- `get_weather_alerts(location)` - Weather alerts

**Use Cases:** Weather queries, planning

---

## 💾 Database Operations

### 7. **SQL Database MCP Server**
**Tools:**
- `execute_query(query, database)` - Execute SQL query
- `list_tables(database)` - List all tables
- `describe_table(table, database)` - Get table schema
- `insert_data(table, data, database)` - Insert records

**Use Cases:** Database queries, data analysis, reporting

### 8. **MongoDB MCP Server**
**Tools:**
- `find_documents(collection, query)` - Find documents
- `insert_document(collection, document)` - Insert document
- `update_document(collection, query, update)` - Update document
- `delete_document(collection, query)` - Delete document

**Use Cases:** NoSQL database operations

---

## 📅 Calendar & Scheduling

### 9. **Calendar MCP Server**
**Tools:**
- `create_event(title, start, end, description)` - Create calendar event
- `list_events(start_date, end_date)` - List events
- `update_event(event_id, changes)` - Update event
- `delete_event(event_id)` - Delete event
- `check_availability(start, end)` - Check free time

**Resources:**
- `calendar://events/today` - Today's events
- `calendar://events/week` - This week's events

**Use Cases:** Meeting scheduling, time management

---

## 🔍 Search & Information

### 10. **Web Search MCP Server**
**Tools:**
- `search_web(query, num_results)` - Web search
- `search_images(query, num_results)` - Image search
- `search_videos(query, num_results)` - Video search
- `search_news(query, num_results)` - News search

**Use Cases:** Research, information gathering

### 11. **Wikipedia MCP Server**
**Tools:**
- `search_wikipedia(query)` - Search Wikipedia
- `get_article(title)` - Get article content
- `get_summary(title)` - Get article summary

**Resources:**
- `wikipedia://article/{title}` - Wikipedia article

**Use Cases:** Research, fact-checking

---

## 💬 Communication

### 12. **SMS MCP Server**
**Tools:**
- `send_sms(to, message)` - Send SMS
- `send_bulk_sms(recipients, message)` - Bulk SMS

**Use Cases:** Notifications, alerts

### 13. **Slack MCP Server**
**Tools:**
- `send_message(channel, message)` - Send Slack message
- `create_channel(name)` - Create channel
- `list_channels()` - List channels
- `upload_file(channel, file_path)` - Upload file

**Use Cases:** Team communication, notifications

### 14. **Discord MCP Server**
**Tools:**
- `send_message(channel_id, message)` - Send message
- `create_embed(channel_id, embed_data)` - Send embed
- `react_to_message(message_id, emoji)` - Add reaction

**Use Cases:** Community management, bots

---

## 📊 Data Analysis & Processing

### 15. **Data Analysis MCP Server**
**Tools:**
- `analyze_csv(path, operations)` - Analyze CSV data
- `generate_chart(data, chart_type)` - Generate charts
- `calculate_statistics(data)` - Calculate stats
- `filter_data(data, conditions)` - Filter data

**Use Cases:** Data analysis, reporting

### 16. **Excel MCP Server**
**Tools:**
- `read_excel(path, sheet)` - Read Excel file
- `write_excel(path, data, sheet)` - Write Excel file
- `format_cells(path, range, format)` - Format cells
- `create_chart(path, data_range)` - Create chart

**Use Cases:** Spreadsheet operations, reporting

---

## 🔐 Security & Authentication

### 17. **Password Manager MCP Server**
**Tools:**
- `store_password(service, username, password)` - Store password
- `retrieve_password(service, username)` - Retrieve password
- `generate_password(length, complexity)` - Generate password
- `list_passwords()` - List stored passwords

**Use Cases:** Password management, security

### 18. **Encryption MCP Server**
**Tools:**
- `encrypt_text(text, key)` - Encrypt text
- `decrypt_text(encrypted, key)` - Decrypt text
- `hash_text(text, algorithm)` - Hash text
- `verify_signature(data, signature, key)` - Verify signature

**Use Cases:** Data security, encryption

---

## 🛒 E-commerce & Shopping

### 19. **Shopping MCP Server**
**Tools:**
- `search_products(query)` - Search products
- `get_product_details(product_id)` - Get product info
- `compare_prices(product_name)` - Compare prices
- `track_order(order_id)` - Track order

**Use Cases:** Shopping assistance, price comparison

---

## 🎵 Media & Entertainment

### 20. **Music MCP Server**
**Tools:**
- `search_songs(query)` - Search songs
- `get_song_info(song_id)` - Get song details
- `create_playlist(name, songs)` - Create playlist
- `play_song(song_id)` - Play song

**Use Cases:** Music management, playlists

### 21. **Video Processing MCP Server**
**Tools:**
- `extract_audio(video_path)` - Extract audio
- `trim_video(video_path, start, end)` - Trim video
- `convert_video_format(video_path, format)` - Convert format
- `get_video_info(video_path)` - Get video metadata

**Use Cases:** Video editing, format conversion

---

## 🏠 Smart Home & IoT

### 22. **Smart Home MCP Server**
**Tools:**
- `control_light(device_id, state)` - Control lights
- `set_temperature(device_id, temperature)` - Set temperature
- `lock_door(device_id)` - Lock/unlock door
- `get_device_status(device_id)` - Get device status

**Use Cases:** Home automation, IoT control

---

## 📝 Note-Taking & Knowledge

### 23. **Note-Taking MCP Server**
**Tools:**
- `create_note(title, content)` - Create note
- `search_notes(query)` - Search notes
- `update_note(note_id, content)` - Update note
- `tag_note(note_id, tags)` - Tag note

**Resources:**
- `notes://note/{note_id}` - Individual note
- `notes://tagged/{tag}` - Notes with tag

**Use Cases:** Knowledge management, note-taking

### 24. **Markdown Processor MCP Server**
**Tools:**
- `parse_markdown(markdown)` - Parse markdown
- `markdown_to_html(markdown)` - Convert to HTML
- `markdown_to_pdf(markdown)` - Convert to PDF
- `extract_headings(markdown)` - Extract headings

**Use Cases:** Documentation, content processing

---

## 🚀 DevOps & Infrastructure

### 25. **Docker MCP Server**
**Tools:**
- `list_containers()` - List containers
- `start_container(container_id)` - Start container
- `stop_container(container_id)` - Stop container
- `build_image(dockerfile_path)` - Build image
- `run_container(image, command)` - Run container

**Use Cases:** Container management, DevOps

### 26. **Git MCP Server**
**Tools:**
- `clone_repository(url, path)` - Clone repo
- `commit_changes(message)` - Commit changes
- `push_changes(remote, branch)` - Push changes
- `create_branch(name)` - Create branch
- `merge_branch(branch)` - Merge branch

**Resources:**
- `git://repository/{path}` - Repository info
- `git://commits/{path}` - Commit history

**Use Cases:** Version control, code management

---

## 🧮 Utilities

### 27. **Calculator MCP Server**
**Tools:**
- `calculate(expression)` - Evaluate expression
- `convert_units(value, from_unit, to_unit)` - Unit conversion
- `solve_equation(equation)` - Solve equation

**Use Cases:** Calculations, conversions

### 28. **Translation MCP Server**
**Tools:**
- `translate_text(text, target_language)` - Translate text
- `detect_language(text)` - Detect language
- `get_supported_languages()` - List languages

**Use Cases:** Translation, multilingual support

### 29. **QR Code MCP Server**
**Tools:**
- `generate_qr_code(data)` - Generate QR code
- `read_qr_code(image_path)` - Read QR code

**Use Cases:** QR code generation, scanning

---

## 🎯 Recommended Starting Points

For your agent, I recommend starting with:

1. **File Manager** - Most versatile, useful for many tasks
2. **Web Scraper** - Great for research and information gathering
3. **Calendar** - Useful for scheduling and time management
4. **Note-Taking** - Helpful for knowledge management
5. **Web Search** - Enhances agent capabilities

Would you like me to help you build any of these? I can create a complete implementation for any of them!
