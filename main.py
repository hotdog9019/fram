import sys
from datetime import datetime


def get_registration_status(registered_teams, max_teams, registration_is_open):
    if not registration_is_open:
        return "Регистрация закрыта организатором"
    if registered_teams >= max_teams:
        return "Регистрация невозможна: лимит команд уже достигнут"
    return "Регистрация доступна"


def calculate_participation_fee(participant_count, fee_per_participant, has_discount):
    total_fee = participant_count * fee_per_participant
    if has_discount:
        return total_fee * 0.8
    return total_fee


def get_submission_status(submitted_at, deadline):
    if submitted_at <= deadline:
        return "Проект сдан вовремя"
    return "Проект сдан после дедлайна"


def calculate_total_score(idea_score, prototype_score, presentation_score):
    return idea_score + prototype_score + presentation_score


def calculate_average_score(total_score):
    return total_score / 3


def get_jury_decision(total_score, passing_score):
    if total_score >= passing_score:
        return f"Проект проходит в финал, итоговый балл: {total_score:.1f}"
    return f"Проект требует доработки, итоговый балл: {total_score:.1f}"


def main():
    sys.stdout.reconfigure(encoding="utf-8")

    hackathon_name = "MIREA Hack 2026"
    team_name = "CodePulse"
    participant_count_text = "4"
    registered_teams_text = "17"
    max_teams_text = "20"
    fee_per_participant_text = "700"
    submitted_at_text = "2026-09-16 18:20"
    deadline_text = "2026-09-16 20:00"
    idea_score_text = "8.5"
    prototype_score_text = "9"
    presentation_score_text = "7.5"
    registration_is_open = True
    has_student_discount = True
    passing_score = 22

    participant_count = int(participant_count_text)
    registered_teams = int(registered_teams_text)
    max_teams = int(max_teams_text)
    fee_per_participant = int(fee_per_participant_text)
    submitted_at = datetime.strptime(submitted_at_text, "%Y-%m-%d %H:%M")
    deadline = datetime.strptime(deadline_text, "%Y-%m-%d %H:%M")
    idea_score = float(idea_score_text)
    prototype_score = float(prototype_score_text)
    presentation_score = float(presentation_score_text)

    registration_status = get_registration_status(
        registered_teams,
        max_teams,
        registration_is_open,
    )
    participation_fee = calculate_participation_fee(
        participant_count,
        fee_per_participant,
        has_student_discount,
    )
    submission_status = get_submission_status(submitted_at, deadline)
    total_score = calculate_total_score(
        idea_score,
        prototype_score,
        presentation_score,
    )
    average_score = calculate_average_score(total_score)
    jury_decision = get_jury_decision(
        total_score,
        passing_score,
    )

    print(f"Хакатон: {hackathon_name}")
    print(f"Команда: {team_name}")
    print(f"Участников в команде: {participant_count}")
    print(f"Зарегистрировано команд: {registered_teams} из {max_teams}")
    print(f"Статус регистрации: {registration_status}")
    print(f"Организационный взнос: {participation_fee:.0f} руб.")
    print(f"Срок сдачи проекта: {deadline.strftime('%d.%m.%Y %H:%M')}")
    print(f"Фактическая сдача: {submitted_at.strftime('%d.%m.%Y %H:%M')}")
    print(f"Статус сдачи: {submission_status}")
    print(f"Средний балл жюри: {average_score:.2f}")
    print(jury_decision)


if __name__ == "__main__":
    main()
