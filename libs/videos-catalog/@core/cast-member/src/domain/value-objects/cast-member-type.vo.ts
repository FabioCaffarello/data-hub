import { ValueObject } from "@data-hub/videos-catalog/@core/@seedwork/domain";
import { Either } from "@data-hub/videos-catalog/@core/@seedwork/domain/utils/either";
import { InvalidCastMemberTypeError } from "../errors/invalid-cast-member-type.error";

enum Types {
  DIRECTOR = 1,
  ACTOR = 2,
}

class CastMemberType extends ValueObject<Types> {
  private constructor(value: Types) {
    super(value);
    this.validate();
  }

  static create(
    value: Types
  ): Either<CastMemberType, InvalidCastMemberTypeError> {
    try {
      return Either.ok(new CastMemberType(value));
    } catch (error) {
      return Either.fail(error);
    }
  }

  private validate() {
    const isValid = this.value === Types.DIRECTOR || this.value === Types.ACTOR;
    if (!isValid) {
      throw new InvalidCastMemberTypeError(this.value);
    }
  }

  static createAnActor() {
    return CastMemberType.create(Types.ACTOR).getOk();
  }

  static createADirector() {
    return CastMemberType.create(Types.DIRECTOR).getOk();
  }
}

export { CastMemberType, Types };
