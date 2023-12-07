// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: xla/service/cpu/backend_config.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_xla_2fservice_2fcpu_2fbackend_5fconfig_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_xla_2fservice_2fcpu_2fbackend_5fconfig_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/generated_enum_reflection.h>
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_xla_2fservice_2fcpu_2fbackend_5fconfig_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_xla_2fservice_2fcpu_2fbackend_5fconfig_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_xla_2fservice_2fcpu_2fbackend_5fconfig_2eproto;
namespace xla {
namespace cpu {
class BackendConfig;
struct BackendConfigDefaultTypeInternal;
extern BackendConfigDefaultTypeInternal _BackendConfig_default_instance_;
class OneDnnMatMulConfig;
struct OneDnnMatMulConfigDefaultTypeInternal;
extern OneDnnMatMulConfigDefaultTypeInternal _OneDnnMatMulConfig_default_instance_;
}  // namespace cpu
}  // namespace xla
PROTOBUF_NAMESPACE_OPEN
template<> ::xla::cpu::BackendConfig* Arena::CreateMaybeMessage<::xla::cpu::BackendConfig>(Arena*);
template<> ::xla::cpu::OneDnnMatMulConfig* Arena::CreateMaybeMessage<::xla::cpu::OneDnnMatMulConfig>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace xla {
namespace cpu {

enum OneDnnMatMulConfig_FusionKind : int {
  OneDnnMatMulConfig_FusionKind_UNDEFINED = 0,
  OneDnnMatMulConfig_FusionKind_BIAS = 1,
  OneDnnMatMulConfig_FusionKind_RELU = 2,
  OneDnnMatMulConfig_FusionKind_TANH = 3,
  OneDnnMatMulConfig_FusionKind_GELU_ERF = 4,
  OneDnnMatMulConfig_FusionKind_GELU_TANH = 5,
  OneDnnMatMulConfig_FusionKind_OneDnnMatMulConfig_FusionKind_INT_MIN_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::min(),
  OneDnnMatMulConfig_FusionKind_OneDnnMatMulConfig_FusionKind_INT_MAX_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::max()
};
bool OneDnnMatMulConfig_FusionKind_IsValid(int value);
constexpr OneDnnMatMulConfig_FusionKind OneDnnMatMulConfig_FusionKind_FusionKind_MIN = OneDnnMatMulConfig_FusionKind_UNDEFINED;
constexpr OneDnnMatMulConfig_FusionKind OneDnnMatMulConfig_FusionKind_FusionKind_MAX = OneDnnMatMulConfig_FusionKind_GELU_TANH;
constexpr int OneDnnMatMulConfig_FusionKind_FusionKind_ARRAYSIZE = OneDnnMatMulConfig_FusionKind_FusionKind_MAX + 1;

const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* OneDnnMatMulConfig_FusionKind_descriptor();
template<typename T>
inline const std::string& OneDnnMatMulConfig_FusionKind_Name(T enum_t_value) {
  static_assert(::std::is_same<T, OneDnnMatMulConfig_FusionKind>::value ||
    ::std::is_integral<T>::value,
    "Incorrect type passed to function OneDnnMatMulConfig_FusionKind_Name.");
  return ::PROTOBUF_NAMESPACE_ID::internal::NameOfEnum(
    OneDnnMatMulConfig_FusionKind_descriptor(), enum_t_value);
}
inline bool OneDnnMatMulConfig_FusionKind_Parse(
    ::PROTOBUF_NAMESPACE_ID::ConstStringParam name, OneDnnMatMulConfig_FusionKind* value) {
  return ::PROTOBUF_NAMESPACE_ID::internal::ParseNamedEnum<OneDnnMatMulConfig_FusionKind>(
    OneDnnMatMulConfig_FusionKind_descriptor(), name, value);
}
// ===================================================================

class BackendConfig final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:xla.cpu.BackendConfig) */ {
 public:
  inline BackendConfig() : BackendConfig(nullptr) {}
  ~BackendConfig() override;
  explicit PROTOBUF_CONSTEXPR BackendConfig(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  BackendConfig(const BackendConfig& from);
  BackendConfig(BackendConfig&& from) noexcept
    : BackendConfig() {
    *this = ::std::move(from);
  }

  inline BackendConfig& operator=(const BackendConfig& from) {
    CopyFrom(from);
    return *this;
  }
  inline BackendConfig& operator=(BackendConfig&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const BackendConfig& default_instance() {
    return *internal_default_instance();
  }
  static inline const BackendConfig* internal_default_instance() {
    return reinterpret_cast<const BackendConfig*>(
               &_BackendConfig_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(BackendConfig& a, BackendConfig& b) {
    a.Swap(&b);
  }
  inline void Swap(BackendConfig* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(BackendConfig* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  BackendConfig* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<BackendConfig>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const BackendConfig& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const BackendConfig& from) {
    BackendConfig::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(BackendConfig* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "xla.cpu.BackendConfig";
  }
  protected:
  explicit BackendConfig(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kOuterDimensionPartitionsFieldNumber = 1,
    kOnednnMatmulConfigFieldNumber = 2,
  };
  // repeated int64 outer_dimension_partitions = 1;
  int outer_dimension_partitions_size() const;
  private:
  int _internal_outer_dimension_partitions_size() const;
  public:
  void clear_outer_dimension_partitions();
  private:
  int64_t _internal_outer_dimension_partitions(int index) const;
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField< int64_t >&
      _internal_outer_dimension_partitions() const;
  void _internal_add_outer_dimension_partitions(int64_t value);
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< int64_t >*
      _internal_mutable_outer_dimension_partitions();
  public:
  int64_t outer_dimension_partitions(int index) const;
  void set_outer_dimension_partitions(int index, int64_t value);
  void add_outer_dimension_partitions(int64_t value);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField< int64_t >&
      outer_dimension_partitions() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< int64_t >*
      mutable_outer_dimension_partitions();

  // .xla.cpu.OneDnnMatMulConfig onednn_matmul_config = 2;
  bool has_onednn_matmul_config() const;
  private:
  bool _internal_has_onednn_matmul_config() const;
  public:
  void clear_onednn_matmul_config();
  const ::xla::cpu::OneDnnMatMulConfig& onednn_matmul_config() const;
  PROTOBUF_NODISCARD ::xla::cpu::OneDnnMatMulConfig* release_onednn_matmul_config();
  ::xla::cpu::OneDnnMatMulConfig* mutable_onednn_matmul_config();
  void set_allocated_onednn_matmul_config(::xla::cpu::OneDnnMatMulConfig* onednn_matmul_config);
  private:
  const ::xla::cpu::OneDnnMatMulConfig& _internal_onednn_matmul_config() const;
  ::xla::cpu::OneDnnMatMulConfig* _internal_mutable_onednn_matmul_config();
  public:
  void unsafe_arena_set_allocated_onednn_matmul_config(
      ::xla::cpu::OneDnnMatMulConfig* onednn_matmul_config);
  ::xla::cpu::OneDnnMatMulConfig* unsafe_arena_release_onednn_matmul_config();

  // @@protoc_insertion_point(class_scope:xla.cpu.BackendConfig)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::RepeatedField< int64_t > outer_dimension_partitions_;
    mutable std::atomic<int> _outer_dimension_partitions_cached_byte_size_;
    ::xla::cpu::OneDnnMatMulConfig* onednn_matmul_config_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_xla_2fservice_2fcpu_2fbackend_5fconfig_2eproto;
};
// -------------------------------------------------------------------

class OneDnnMatMulConfig final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:xla.cpu.OneDnnMatMulConfig) */ {
 public:
  inline OneDnnMatMulConfig() : OneDnnMatMulConfig(nullptr) {}
  ~OneDnnMatMulConfig() override;
  explicit PROTOBUF_CONSTEXPR OneDnnMatMulConfig(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  OneDnnMatMulConfig(const OneDnnMatMulConfig& from);
  OneDnnMatMulConfig(OneDnnMatMulConfig&& from) noexcept
    : OneDnnMatMulConfig() {
    *this = ::std::move(from);
  }

  inline OneDnnMatMulConfig& operator=(const OneDnnMatMulConfig& from) {
    CopyFrom(from);
    return *this;
  }
  inline OneDnnMatMulConfig& operator=(OneDnnMatMulConfig&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const OneDnnMatMulConfig& default_instance() {
    return *internal_default_instance();
  }
  static inline const OneDnnMatMulConfig* internal_default_instance() {
    return reinterpret_cast<const OneDnnMatMulConfig*>(
               &_OneDnnMatMulConfig_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(OneDnnMatMulConfig& a, OneDnnMatMulConfig& b) {
    a.Swap(&b);
  }
  inline void Swap(OneDnnMatMulConfig* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(OneDnnMatMulConfig* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  OneDnnMatMulConfig* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<OneDnnMatMulConfig>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const OneDnnMatMulConfig& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const OneDnnMatMulConfig& from) {
    OneDnnMatMulConfig::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(OneDnnMatMulConfig* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "xla.cpu.OneDnnMatMulConfig";
  }
  protected:
  explicit OneDnnMatMulConfig(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  typedef OneDnnMatMulConfig_FusionKind FusionKind;
  static constexpr FusionKind UNDEFINED =
    OneDnnMatMulConfig_FusionKind_UNDEFINED;
  static constexpr FusionKind BIAS =
    OneDnnMatMulConfig_FusionKind_BIAS;
  static constexpr FusionKind RELU =
    OneDnnMatMulConfig_FusionKind_RELU;
  static constexpr FusionKind TANH =
    OneDnnMatMulConfig_FusionKind_TANH;
  static constexpr FusionKind GELU_ERF =
    OneDnnMatMulConfig_FusionKind_GELU_ERF;
  static constexpr FusionKind GELU_TANH =
    OneDnnMatMulConfig_FusionKind_GELU_TANH;
  static inline bool FusionKind_IsValid(int value) {
    return OneDnnMatMulConfig_FusionKind_IsValid(value);
  }
  static constexpr FusionKind FusionKind_MIN =
    OneDnnMatMulConfig_FusionKind_FusionKind_MIN;
  static constexpr FusionKind FusionKind_MAX =
    OneDnnMatMulConfig_FusionKind_FusionKind_MAX;
  static constexpr int FusionKind_ARRAYSIZE =
    OneDnnMatMulConfig_FusionKind_FusionKind_ARRAYSIZE;
  static inline const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor*
  FusionKind_descriptor() {
    return OneDnnMatMulConfig_FusionKind_descriptor();
  }
  template<typename T>
  static inline const std::string& FusionKind_Name(T enum_t_value) {
    static_assert(::std::is_same<T, FusionKind>::value ||
      ::std::is_integral<T>::value,
      "Incorrect type passed to function FusionKind_Name.");
    return OneDnnMatMulConfig_FusionKind_Name(enum_t_value);
  }
  static inline bool FusionKind_Parse(::PROTOBUF_NAMESPACE_ID::ConstStringParam name,
      FusionKind* value) {
    return OneDnnMatMulConfig_FusionKind_Parse(name, value);
  }

  // accessors -------------------------------------------------------

  enum : int {
    kFusedOpsFieldNumber = 3,
  };
  // repeated .xla.cpu.OneDnnMatMulConfig.FusionKind fused_ops = 3;
  int fused_ops_size() const;
  private:
  int _internal_fused_ops_size() const;
  public:
  void clear_fused_ops();
  private:
  ::xla::cpu::OneDnnMatMulConfig_FusionKind _internal_fused_ops(int index) const;
  void _internal_add_fused_ops(::xla::cpu::OneDnnMatMulConfig_FusionKind value);
  ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>* _internal_mutable_fused_ops();
  public:
  ::xla::cpu::OneDnnMatMulConfig_FusionKind fused_ops(int index) const;
  void set_fused_ops(int index, ::xla::cpu::OneDnnMatMulConfig_FusionKind value);
  void add_fused_ops(::xla::cpu::OneDnnMatMulConfig_FusionKind value);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>& fused_ops() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>* mutable_fused_ops();

  // @@protoc_insertion_point(class_scope:xla.cpu.OneDnnMatMulConfig)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::RepeatedField<int> fused_ops_;
    mutable std::atomic<int> _fused_ops_cached_byte_size_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_xla_2fservice_2fcpu_2fbackend_5fconfig_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// BackendConfig

// repeated int64 outer_dimension_partitions = 1;
inline int BackendConfig::_internal_outer_dimension_partitions_size() const {
  return _impl_.outer_dimension_partitions_.size();
}
inline int BackendConfig::outer_dimension_partitions_size() const {
  return _internal_outer_dimension_partitions_size();
}
inline void BackendConfig::clear_outer_dimension_partitions() {
  _impl_.outer_dimension_partitions_.Clear();
}
inline int64_t BackendConfig::_internal_outer_dimension_partitions(int index) const {
  return _impl_.outer_dimension_partitions_.Get(index);
}
inline int64_t BackendConfig::outer_dimension_partitions(int index) const {
  // @@protoc_insertion_point(field_get:xla.cpu.BackendConfig.outer_dimension_partitions)
  return _internal_outer_dimension_partitions(index);
}
inline void BackendConfig::set_outer_dimension_partitions(int index, int64_t value) {
  _impl_.outer_dimension_partitions_.Set(index, value);
  // @@protoc_insertion_point(field_set:xla.cpu.BackendConfig.outer_dimension_partitions)
}
inline void BackendConfig::_internal_add_outer_dimension_partitions(int64_t value) {
  _impl_.outer_dimension_partitions_.Add(value);
}
inline void BackendConfig::add_outer_dimension_partitions(int64_t value) {
  _internal_add_outer_dimension_partitions(value);
  // @@protoc_insertion_point(field_add:xla.cpu.BackendConfig.outer_dimension_partitions)
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField< int64_t >&
BackendConfig::_internal_outer_dimension_partitions() const {
  return _impl_.outer_dimension_partitions_;
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField< int64_t >&
BackendConfig::outer_dimension_partitions() const {
  // @@protoc_insertion_point(field_list:xla.cpu.BackendConfig.outer_dimension_partitions)
  return _internal_outer_dimension_partitions();
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField< int64_t >*
BackendConfig::_internal_mutable_outer_dimension_partitions() {
  return &_impl_.outer_dimension_partitions_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField< int64_t >*
BackendConfig::mutable_outer_dimension_partitions() {
  // @@protoc_insertion_point(field_mutable_list:xla.cpu.BackendConfig.outer_dimension_partitions)
  return _internal_mutable_outer_dimension_partitions();
}

// .xla.cpu.OneDnnMatMulConfig onednn_matmul_config = 2;
inline bool BackendConfig::_internal_has_onednn_matmul_config() const {
  return this != internal_default_instance() && _impl_.onednn_matmul_config_ != nullptr;
}
inline bool BackendConfig::has_onednn_matmul_config() const {
  return _internal_has_onednn_matmul_config();
}
inline void BackendConfig::clear_onednn_matmul_config() {
  if (GetArenaForAllocation() == nullptr && _impl_.onednn_matmul_config_ != nullptr) {
    delete _impl_.onednn_matmul_config_;
  }
  _impl_.onednn_matmul_config_ = nullptr;
}
inline const ::xla::cpu::OneDnnMatMulConfig& BackendConfig::_internal_onednn_matmul_config() const {
  const ::xla::cpu::OneDnnMatMulConfig* p = _impl_.onednn_matmul_config_;
  return p != nullptr ? *p : reinterpret_cast<const ::xla::cpu::OneDnnMatMulConfig&>(
      ::xla::cpu::_OneDnnMatMulConfig_default_instance_);
}
inline const ::xla::cpu::OneDnnMatMulConfig& BackendConfig::onednn_matmul_config() const {
  // @@protoc_insertion_point(field_get:xla.cpu.BackendConfig.onednn_matmul_config)
  return _internal_onednn_matmul_config();
}
inline void BackendConfig::unsafe_arena_set_allocated_onednn_matmul_config(
    ::xla::cpu::OneDnnMatMulConfig* onednn_matmul_config) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.onednn_matmul_config_);
  }
  _impl_.onednn_matmul_config_ = onednn_matmul_config;
  if (onednn_matmul_config) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:xla.cpu.BackendConfig.onednn_matmul_config)
}
inline ::xla::cpu::OneDnnMatMulConfig* BackendConfig::release_onednn_matmul_config() {
  
  ::xla::cpu::OneDnnMatMulConfig* temp = _impl_.onednn_matmul_config_;
  _impl_.onednn_matmul_config_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::xla::cpu::OneDnnMatMulConfig* BackendConfig::unsafe_arena_release_onednn_matmul_config() {
  // @@protoc_insertion_point(field_release:xla.cpu.BackendConfig.onednn_matmul_config)
  
  ::xla::cpu::OneDnnMatMulConfig* temp = _impl_.onednn_matmul_config_;
  _impl_.onednn_matmul_config_ = nullptr;
  return temp;
}
inline ::xla::cpu::OneDnnMatMulConfig* BackendConfig::_internal_mutable_onednn_matmul_config() {
  
  if (_impl_.onednn_matmul_config_ == nullptr) {
    auto* p = CreateMaybeMessage<::xla::cpu::OneDnnMatMulConfig>(GetArenaForAllocation());
    _impl_.onednn_matmul_config_ = p;
  }
  return _impl_.onednn_matmul_config_;
}
inline ::xla::cpu::OneDnnMatMulConfig* BackendConfig::mutable_onednn_matmul_config() {
  ::xla::cpu::OneDnnMatMulConfig* _msg = _internal_mutable_onednn_matmul_config();
  // @@protoc_insertion_point(field_mutable:xla.cpu.BackendConfig.onednn_matmul_config)
  return _msg;
}
inline void BackendConfig::set_allocated_onednn_matmul_config(::xla::cpu::OneDnnMatMulConfig* onednn_matmul_config) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete _impl_.onednn_matmul_config_;
  }
  if (onednn_matmul_config) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(onednn_matmul_config);
    if (message_arena != submessage_arena) {
      onednn_matmul_config = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, onednn_matmul_config, submessage_arena);
    }
    
  } else {
    
  }
  _impl_.onednn_matmul_config_ = onednn_matmul_config;
  // @@protoc_insertion_point(field_set_allocated:xla.cpu.BackendConfig.onednn_matmul_config)
}

// -------------------------------------------------------------------

// OneDnnMatMulConfig

// repeated .xla.cpu.OneDnnMatMulConfig.FusionKind fused_ops = 3;
inline int OneDnnMatMulConfig::_internal_fused_ops_size() const {
  return _impl_.fused_ops_.size();
}
inline int OneDnnMatMulConfig::fused_ops_size() const {
  return _internal_fused_ops_size();
}
inline void OneDnnMatMulConfig::clear_fused_ops() {
  _impl_.fused_ops_.Clear();
}
inline ::xla::cpu::OneDnnMatMulConfig_FusionKind OneDnnMatMulConfig::_internal_fused_ops(int index) const {
  return static_cast< ::xla::cpu::OneDnnMatMulConfig_FusionKind >(_impl_.fused_ops_.Get(index));
}
inline ::xla::cpu::OneDnnMatMulConfig_FusionKind OneDnnMatMulConfig::fused_ops(int index) const {
  // @@protoc_insertion_point(field_get:xla.cpu.OneDnnMatMulConfig.fused_ops)
  return _internal_fused_ops(index);
}
inline void OneDnnMatMulConfig::set_fused_ops(int index, ::xla::cpu::OneDnnMatMulConfig_FusionKind value) {
  _impl_.fused_ops_.Set(index, value);
  // @@protoc_insertion_point(field_set:xla.cpu.OneDnnMatMulConfig.fused_ops)
}
inline void OneDnnMatMulConfig::_internal_add_fused_ops(::xla::cpu::OneDnnMatMulConfig_FusionKind value) {
  _impl_.fused_ops_.Add(value);
}
inline void OneDnnMatMulConfig::add_fused_ops(::xla::cpu::OneDnnMatMulConfig_FusionKind value) {
  _internal_add_fused_ops(value);
  // @@protoc_insertion_point(field_add:xla.cpu.OneDnnMatMulConfig.fused_ops)
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>&
OneDnnMatMulConfig::fused_ops() const {
  // @@protoc_insertion_point(field_list:xla.cpu.OneDnnMatMulConfig.fused_ops)
  return _impl_.fused_ops_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>*
OneDnnMatMulConfig::_internal_mutable_fused_ops() {
  return &_impl_.fused_ops_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>*
OneDnnMatMulConfig::mutable_fused_ops() {
  // @@protoc_insertion_point(field_mutable_list:xla.cpu.OneDnnMatMulConfig.fused_ops)
  return _internal_mutable_fused_ops();
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace cpu
}  // namespace xla

PROTOBUF_NAMESPACE_OPEN

template <> struct is_proto_enum< ::xla::cpu::OneDnnMatMulConfig_FusionKind> : ::std::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::xla::cpu::OneDnnMatMulConfig_FusionKind>() {
  return ::xla::cpu::OneDnnMatMulConfig_FusionKind_descriptor();
}

PROTOBUF_NAMESPACE_CLOSE

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_xla_2fservice_2fcpu_2fbackend_5fconfig_2eproto
