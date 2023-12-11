SELECT m_model.model_number,
    m_model.model_name,
    CAST(
        AVG(
            TIME_TO_SEC(
                TIMEDIFF(
                    subquery.max_process_time,
                    subquery.min_process_time
                )
            )
        ) AS SIGNED
    ) AS average_time_diff
FROM m_model
    LEFT JOIN (
        SELECT m_work.serial_number,
            m_work.model_number,
            MIN(t_work_tracking.process_time) AS min_process_time,
            MAX(t_work_tracking.process_time) AS max_process_time
        FROM m_work
            JOIN t_work_tracking ON t_work_tracking.serial_number = m_work.serial_number
            JOIN m_process ON t_work_tracking.process_id = m_process.process_id
            JOIN (
                SELECT MIN(process_id) AS min_id,
                    MAX(process_id) AS max_id
                FROM m_process
            ) AS process_range
        WHERE m_process.process_id = process_range.min_id
            OR m_process.process_id = process_range.max_id
        GROUP BY m_work.serial_number
    ) AS subquery ON m_model.model_number = subquery.model_number
    JOIN m_processing ON m_model.processing_id = m_processing.processing_id
WHERE m_processing.invisible = 1
GROUP BY m_model.model_number;