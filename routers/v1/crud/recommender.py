import numpy as np
from fastapi import HTTPException
from jose import JWTError, jwt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import (cosine_similarity, linear_kernel,
                                      pairwise_distances)
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy.orm import Session

from config import JWT_KEY
from logger import setup_logging
from routers.v1.crud import helper

logger = setup_logging()


# JWT token verification
def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=["HS256"])
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        else:
            return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# function to find similar temps and return list of temps
def recommend_temps(
    input_data, numerical_features, new_df, df, scaler, metric="cosine"
):
    try:
        # Normalize input data if needed (assuming scaler is defined)
        input_array = np.array(
            [[input_data[feature] for feature in numerical_features]]
        )
        input_array = scaler.transform(input_array)

        # Calculate pairwise distances with input data
        if metric == "cosine":
            distances = (
                1 - cosine_similarity(input_array, new_df[numerical_features])[0]
            )
        elif metric == "jaccard":
            distances = pairwise_distances(
                input_array, new_df[numerical_features], metric="jaccard"
            )[0]
        elif metric == "manhattan":
            distances = pairwise_distances(
                input_array, new_df[numerical_features], metric="manhattan"
            )[0]
        elif metric == "minkowski":
            distances = pairwise_distances(
                input_array, new_df[numerical_features], metric="minkowski"
            )[0]
        elif metric == "euclidean":
            distances = pairwise_distances(
                input_array, new_df[numerical_features], metric="euclidean"
            )[0]
        else:
            raise ValueError(
                "Invalid metric. Choose from 'cosine', 'jaccard', 'manhattan', 'minkowski', 'euclidean'."
            )

        # Sort temps based on distances
        temp_indices = np.argsort(distances)[:5]
        # similarity_scores = [1 - distances[i] for i in temp_indices]
        tempids = df.iloc[temp_indices]["tempid"].values
        tempid_list = [str(x) for x in tempids]
        return tempid_list
    except Exception as e:
        logger.error(f"Error in recommend_temps function: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# API temp recommendation abstraction function
def temp_recommender(
    # request: Request,
    authorization: str,
    city: str,
    state: str,
    speciality: str,
    certificate: str,
    db: Session,
):
    # token = request.headers.get("authorization")
    token = authorization
    if not token or not token.startswith("Bearer "):
        logger.error("Missing or invalid token")
        return HTTPException(status_code=401, detail="Missing or invalid token")
    token = token.split(" ")[1]
    email = verify_token(token)
    try:
        logger.info(f"Validated user {email}")
        logger.info(
            f"Input for temps given by {email}:- {[city,state,speciality,certificate]}"
        )
        temp_df = helper.fetch_temps_data_to_dataframe(db)
        new_temp_df = helper.fetch_temps_data_to_dataframe(db)
        badge_data = helper.fetch_badge_data_from_db(db)
        scaler = MinMaxScaler()
        numerical_features = ["attendance_score", "on_time_rate"]
        new_temp_df[numerical_features] = scaler.fit_transform(
            new_temp_df[numerical_features]
        )
        temp_recommendation_payload = {"data": {"temps": {}}}
        for badge in badge_data:
            input_data = {
                "attendance_score": badge.attendance_score_threshold,
                "on_time_rate": badge.on_time_threshold,
            }
            recommended_temps = recommend_temps(
                input_data=input_data,
                numerical_features=numerical_features,
                new_df=new_temp_df,
                df=temp_df,
                scaler=scaler,
                metric="minkowski",
            )
            # badge_wise_recommendations = {badge.badge_name: recommended_temps}
            temp_recommendation_payload["data"]["temps"][
                badge.badge_name
            ] = recommended_temps
        if not temp_recommendation_payload["data"]["temps"]:
            logger.error(
                "No recommendations available for the specified city and state"
            )
            return HTTPException(
                status_code=404,
                detail="No recommendations available for the specified city and state",
            )
        logger.info(
            f"Temps recommendations {temp_recommendation_payload} for user {email}"
        )
        return temp_recommendation_payload
    except Exception as e:
        logger.error(f"Error in temp_recommender endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# function to recommend shifts from database
def recommend_shifts(
    shift_df, tfidf_vectorizer, tfidf_matrix, certificate, city, state, speciality
):
    try:
        query_text = f"{speciality} {certificate} {city}{state}"
        query_vec = tfidf_vectorizer.transform([query_text])
        sim_scores = linear_kernel(query_vec, tfidf_matrix).flatten()
        top_indices = sim_scores.argsort()[-5:][::-1]
        shift_ids = shift_df.iloc[top_indices]["id"].values
        shift_list = [str(x) for x in shift_ids]
        return shift_list
    except Exception as e:
        logger.error(f"Error in recommend_shifts function: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# API shift recommender abstraction function
def shift_recommender(
    # request: Request,
    authorization: str,
    city: str,
    state: str,
    speciality: str,
    certificate: str,
    db: Session,
):
    # token = request.headers.get("authorization") # for further refrence
    token = authorization
    if not token or not token.startswith("Bearer "):
        logger.error("Missing or invalid token")
        return HTTPException(status_code=401, detail="Missing or invalid token")
    token = token.split(" ")[1]
    email = verify_token(token)
    try:
        logger.info(f"Validated user {email}")
        logger.info(
            f"Input for shifts given by {email}:- {[city,state,speciality,certificate]}"
        )
        shift_df = helper.fetch_shift_data_to_dataframe(db)
        shift_df["text"] = (
            shift_df["speciality"]
            + " "
            + shift_df["certification"]
            + " "
            + shift_df["city"]
            + " "
            + shift_df["state"]
        )
        tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf_vectorizer.fit_transform(shift_df["text"])
        shift_recommendation_payload = {"data": {"shift": None}}
        recommended_shifts = recommend_shifts(
            shift_df=shift_df,
            tfidf_vectorizer=tfidf_vectorizer,
            tfidf_matrix=tfidf_matrix,
            certificate=certificate,
            city=city,
            state=state,
            speciality=speciality,
        )
        shift_recommendation_payload["data"]["shift"] = recommended_shifts
        if not shift_recommendation_payload["data"]["shift"]:
            logger.error(
                "No recommendations available for the specified city, state, speciality or certification"
            )
            return HTTPException(
                status_code=404,
                detail="No recommendations available for the specified city, state, speciality or certification",
            )
        logger.info(
            f"shifts recommendations {shift_recommendation_payload} for user {email}"
        )
        return shift_recommendation_payload
    except Exception as e:
        logger.error(f"Error in shift_recommender endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
