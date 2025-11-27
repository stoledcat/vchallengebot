get_stat_of_day = """
SELECT u.user_id, u.username, u.first_name, u.last_name
FROM users u
JOIN events e ON u.user_id = e.user_id AND e.chat_id = ?
WHERE u.is_member = 1
AND u.user_id NOT IN (
    SELECT user_id
    FROM events
    WHERE chat_id = ?
    AND DATE(created_at) = DATE('now', 'localtime')
)
"""
